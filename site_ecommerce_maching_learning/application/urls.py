from django.urls import path
from application.views import index, product_list_view, category_list_view, category_product_list_view, vendor_list_view, vendor_detail_view, product_detail_view, ajax_add_review, search_view, filter_product, recommandation_view, about_view, account, conta
#from django.conf.urls import url, include

name_app = "Lounge_application"

urlpatterns = [
    #homepage
    path("", index, name="index") ,   #if we don't set the path so it's the main page !   
    path("products/", product_list_view, name="product-list"),
    path("products/<pid>/", product_detail_view, name="product-detail"),

    #category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),     

    #vendor 
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendors/<vid>/", vendor_detail_view, name="vendor-detail"),

    #review
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),

    #search
    path("search/", search_view, name="search"),
    #url(r'^search/', include('haystack.urls')),

    #filter product 
    path("filter-products/", filter_product, name="filter-product"),
    
    #recommandation
    path("recommandation/", recommandation_view, name="Recommandation-product"),

    #About
    path("about/", about_view, name="about"),
    path("account/", account, name='account'),
    path("contact/", conta, name="contact"),
]