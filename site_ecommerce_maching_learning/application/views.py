from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from application.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, WishList, Address
from application.forms import ProductReviewForm
from django.template.loader import render_to_string
import csv
import pandas as pd
from application.recommandation import get_recommandation

from django.contrib import messages


def index(request):
    # Charger les données du fichier CSV dans un DataFrame
    with open('application/prepro19.csv', 'r') as file:
        reader = csv.DictReader(file)
        products = pd.DataFrame(list(reader))
    
    print(products.shape)

    products.drop_duplicates(subset='Product_ID', inplace=True)

    print(products.shape)

    # Filtrer les produits avec une note de 5.0
    products = products[products['Rating'] == '5.0']

    # Convertir le DataFrame filtré en liste de dictionnaires
    products_list = products.to_dict('records')
    

    '''for product in products_list:
        print(product['Rating'])'''

    # Passer la liste de produits filtrés à votre template
    context = {
        'products': products_list
    }

    # Rendre le template avec le contexte
    return render(request, 'htmli/index.html', context)



def product_list_view(request, category_slug=None):
    # Read data from CSV file
    with open('application/prepro19.csv', 'r') as file:
        reader = csv.DictReader(file)
        products = pd.DataFrame(list(reader))
    
    products.drop_duplicates(subset='Product_ID', inplace=True)

    products_list = products.to_dict('records')

    context = {
        'products': products_list
    }
    return render(request, 'htmli/product-list.html', context)









'''def product_list_view(request, category_slug=None):
    
    products = Product.objects.filter(product_status='published').order_by("-id")

    context = {
        'products': products
    }
    return render(request, 'htmli/product-list.html', context)'''

def category_list_view(request):

    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request, 'htmli/category-list.html', context)


def category_product_list_view(request, cid):

    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'htmli/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors":vendors,
    }
    return render(request, 'htmli/vendor-list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(product_status='published', vendor=vendor)

    context = {
        "vendor":vendor,
        "products":products,
    }
    return render(request, 'htmli/vendor-detail.html', context)



def product_detail_view(request, pid):
    with open('application/prepro19.csv', 'r') as file:
        reader = csv.DictReader(file)
        products = list(reader)

    # Iterate over the products list to find the product with the specified ID
    product = None
    for p in products:
        if p['Product_ID'] == pid:
            product = p
            break

    # Check if the product exists
    if product:
        # Assuming 'ProductReview' model is available and it has a ForeignKey relationship with 'Product'
        # You should adjust this query according to your actual model
        reviews = ProductReview.objects.filter(product=pid).order_by('date')
        review_form = ProductReviewForm()

        make_review = True

        if request.user.is_authenticated:
            user_review_count = ProductReview.objects.filter(user=request.user, product=pid).count()

            if user_review_count > 0:
                make_review = False

        # Getting the average rating of the product
        avg_rating = ProductReview.objects.filter(product=pid).aggregate(rating=Avg('rating'))

        context = {
            "product": product,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'review_form': review_form,
            'make_review': make_review
        }
        return render(request, 'htmli/product-detail.html', context)
    else:
        # Handle case where product with specified ID is not found
        return render(request, 'htmli/product-not-found.html')



'''def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:1]
    p_images = product.p_images.all()
    reviews = ProductReview.objects.filter(product=product).order_by('date')
    review_form = ProductReviewForm()

    make_review = True 

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False
    # getting the average rating of the product
    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    context = {
        "product":product,
        'p_images': p_images,
        'products': products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'make_review': make_review
    }
    return render(request, 'htmli/product-detail.html', context)'''



def ajax_add_review(request, pid):
    # Assuming 'prepro20.csv' contains the product data
    with open('application/prepro19.csv', 'r') as file:
        reader = csv.DictReader(file)
        products = list(reader)

    # Iterate over the products list to find the product with the specified ID
    product = None
    for p in products:
        if p['Product_ID'] == pid:
            product = p
            break

    if not product:
        return JsonResponse({'bool': False, 'error': 'Product not found.'}, status=404)

    user = request.user 

    review_text = request.POST.get('review', '')
    rating = request.POST.get('rating', '')

    if not review_text or not rating:
        return JsonResponse({'bool': False, 'error': 'Review or rating missssing.'}, status=400)

    try:
        rating = float(rating)
    except ValueError:
        return JsonResponse({'bool': False, 'error': 'Invalid rating format.'}, status=400)

    # Create the review without requiring an existing product object
    review = ProductReview.objects.create(
        product=pid,  # Assuming ProductReview model has a ForeignKey to the product ID
        user=user,
        review=review_text,
        rating=rating,
    )

    # Calculate the average rating
    average_rating = ProductReview.objects.filter(product=pid).aggregate(avg_rating=Avg("rating"))['avg_rating']

    context = {
        'user': user.username,
        'review': review_text,
        'rating': rating,
    }

    return JsonResponse({
        'bool': True,
        'context': context,
        'average_rating': average_rating
    })


'''def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user 

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
       {
         'bool': True,
        'context': context,
        'average_reviews': average_reviews
       }
    )'''


def search_view(request):
    query = request.GET.get("q")
    with open('application/prepro19.csv', 'r') as file:
        reader = csv.DictReader(file)
        products_df = pd.DataFrame(list(reader))

    # Drop duplicates based on 'Product_ID'
    products_df.drop_duplicates(subset='Product_ID', inplace=True)

    # Convert DataFrame to list of dictionaries
    products_list = products_df.to_dict('records')

    # Filtering products based on the query
    if query:
        filtered_products = [product for product in products_list if (query in (product['Product_name'] or product['Product_name']))] 
    else:
        filtered_products = []

    context = {
        "products": filtered_products,
        "query": query,
    }
    return render(request, "htmli/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")


    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() 
    else:
        products = Product.objects.filter(product_status="published").distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct() 
    else:
        products = Product.objects.filter(product_status="published").distinct()   
    
       

    
    data = render_to_string("htmli/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})





##############################################################################################################

####################################################Recommandation#################################################


def recommandation_view(request):
    user_id = request.user.id

    if not user_id:
        messages.info(request, "'error': 'User not authenticated'") 
        return redirect("index")
    
    csv_data = pd.read_csv('application/prepro19.csv')
    csv_data =pd.DataFrame(csv_data)

    user_ratings = ProductReview.objects.filter(user=user_id).values_list('user','product', 'rating')
    
    user_rating_df = pd.DataFrame(user_ratings, columns=['User_ID', 'Product_ID', 'Rating'])
    #print(user_rating_df.head(20))
    if user_rating_df.shape[0] <= 4: 
        messages.info(request, "Please rate atleast 5 books") 
        return redirect("index")

    else:
        #if user_rating_df :
        concat_data = pd.concat([user_rating_df, csv_data])

        #print(concat_data)

        liste_product = get_recommandation(concat_data, user_id, 10)
        print(liste_product)

        liste =[]

        for pp in liste_product :
            liste.append(pp.iid)

        print(liste)

        # get the origin dataset :

        # List to store the filtered rows
        filtered_products = []

        # Set to store unique product IDs
        unique_product_ids = set()

        # List to store the filtered rows
        filtered_products = []

        # Open the CSV file and read its contents
        with open('application/prepro19.csv', 'r') as file:
            reader = csv.DictReader(file)
                
            # Iterate over each row in the CSV
            for row in reader:
                # Check if the product ID is in the list of IDs to keep
                if row['Product_ID'] in liste :
                    # Check if the product ID has not been encountered before
                    if row['Product_ID'] not in unique_product_ids:
                        # If yes, add the row to the filtered list and mark the product ID as encountered
                        filtered_products.append(row)
                        unique_product_ids.add(row['Product_ID'])

    context = {
        'filtered_products': filtered_products
    }



    return render(request, "htmli/Recommandation-product.html", context)



def about_view(request):
    return render(request, "htmli/about.html")


def account(request):
    user_id = request.user
    context = {
        'user': user_id
    }
    
    return render(request, "htmli/account.html",context)


def conta(request):
    return render(request, "htmli/contact.html")



