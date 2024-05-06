from django.shortcuts import render
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User

#User = settings.AUTH_USER_MODEL


def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)  #la creation de new user est faite par le formulaire
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            # passowrd1 car on a deux une par la meme requete
            login(request, new_user)
            return redirect('index') #redirection vers la page d'accueil
    
    else:
        form = UserRegistrationForm()
        print("User cannot be registred")

    context = {
        'form' : form ,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("index")
    
    if request.method == "POST":
        email = request.POST.get("email") # peanuts@gmail.com
        password = request.POST.get("password1") # getmepeanuts

        try:
            user = User.objects.get(email=email)
            #user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                next_url = request.GET.get("next", 'index')
                return redirect(next_url)
            else:
                messages.warning(request, "User Does Not Exist, create an account.")
    
        except:
            messages.warning(request, f"User with {email} does not exist")
        

    
    return render(request, "userauths/sign-in.html")
def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out successfully.")
    return redirect("userauths:sign-in")


            

