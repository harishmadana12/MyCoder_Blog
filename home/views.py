from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
# HTML pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        print(name, email, phone, content)
        if len(name)==0 or len(email)==0 or len(phone)==0 or len(content)==0:
            messages.error(request, "Please fill all the information properly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been submitted. Thank you.")
    return render(request, 'home/contact.html')

# Authentication APIs 
def search(request):
    query=request.GET['query']
    if len(query) > 40:
        allposts = Post.objects.none()
    else:
        allpostsTitle = Post.objects.filter(title__icontains=query)
        allpostsContent = Post.objects.filter(content__icontains=query)
        allposts1 = allpostsTitle.union(allpostsContent)
        allpostsAuthor = Post.objects.filter(author__icontains=query)
        allposts = allposts1.union(allpostsAuthor)
    if allposts.count()== 0:
        messages.warning(request, "No search results found, please refine your query")
    else:
        messages.success(request, "Your search result are here")
    params = {'allposts':allposts, 'query':query}
    return render(request, 'home/search.html', params)

def handleSignUp(request):
    # Getting the output from HTML Forms
    if request.method=='POST':
        usrname = request.POST['usrname']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validations
        if len(usrname) > 10:
            messages.error(request, "Your username should not exceed the length 10")
            return redirect('/')
        if not usrname.isalnum():
            messages.error(request, "Username should be Alphanumeric only")
            return redirect('/')
        if User.objects.filter(username=usrname).exists():
            messages.error(request, "Username alredy exists. Try different username")
            return redirect('/')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Id alredy exists. Try different email id")
            return redirect('/')
        if password1 != password2:
            messages.error(request, "Password not matching")
            return redirect('/')
        
        # Adding to Database
        myUser = User.objects.create_user(usrname, email, password1)
        myUser.first_name=f_name
        myUser.last_name=l_name
        myUser.save()
        messages.success(request, "Congratulations! Your MyCoder account is successfully created.")
        return redirect('/')
    else:
        return HttpResponse('Error: 404 - Page not found')

def handleLogin(request):
    if request.method=='POST':
        usrname = request.POST['loguser']
        password = request.POST['password']

        user = authenticate(username=usrname, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect('/')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('/')