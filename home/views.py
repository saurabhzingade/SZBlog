from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
import datetime

# Create your views here.
def home(request):
    current_datetime = datetime.datetime.now()
    context={'current_datetime':current_datetime}
    return render(request,'home/home.html',context)
    
    #return HttpResponse("This is home")

def about(request):
    return render(request,'home/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content=request.POST['content']
        if(len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4):
            messages.error(request,'Enter the form correctly')
        else:
            messages.success(request,'Your Message is saved. We will get back to you soon!')
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
    return render(request,'home/contact.html')


def search(request):
    query=request.GET['query']
    #allPosts = Post.objects.all()
    if len(query)>80:
        allPosts=Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request,"No Search results found! Please insert correct query!")

    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)


#Authenticate Login codes

def handleSignup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']       
        
        #Checks for error inputs
        if len(username)>10:
            messages.error(request,"Username must be 15 characters")
            return redirect("/")
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
            return redirect("/")
        if not username.isalnum():
            messages.error(request,"Username should only have letters and numbers!")
            return redirect("/")



        #Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"You SZBlog Account is successfully created")
        return redirect("/")
    else:
        messages.error(request,"Please check one of the fields while registration!")
        return HttpResponse('404-Not found!')

def handlelogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']       
        user = authenticate(username=loginusername,password= loginpass)

        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfull!")
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials. Please Try Again!")
            return redirect("home")
    return HttpResponse('404-Not Found')
    
def handlelogout(request):   
    logout(request)
    messages.success(request,"Logout Successfull!")
    return redirect("home")

