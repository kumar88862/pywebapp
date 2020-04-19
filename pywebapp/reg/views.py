from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
import boto3
from core import models
def signup(request):
    if request.method=="POST":
        username=request.POST['Username']
        firstname=request.POST['Firstname']
        lastname=request.POST['Lastname']
        email=request.POST['Email']
        password=request.POST['Password']
        password1=request.POST['ConfirmPassword']
        print(username,firstname,lastname,email,password,password1)
        if User.objects.filter(email=email).exists():
            print('resended')
            messages.info(request,'*email already exists')
            return render(request,'index.html',{'data':'1'})
        if User.objects.filter(username=username).exists():
            print('resended')
            messages.info(request,'*username already exists')
            return render(request,'index.html',{'data':'1'})
        print("************")
        s=email
        s=s.replace('.','d')
        s=s.replace('@','a')
        u=username.replace(' ','s')
        bucket_name=u+'kumar'+s
        print(bucket_name)
        bucket_name=bucket_name.lower()
        print("*************")
        client=boto3.client('s3')
        print("loading .................")
        response = client.create_bucket(ACL='private',Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        print('**************')
        print(response)
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        users=models.My_users(username=username,email=email,firstname=firstname,lastname=lastname)
        users.save()

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            #data=models.File.objects.filter(username=request.user.username)

            return redirect('/mybooks')
        else:
            return render(request,'index.html')


    else:
        return render(request,'index.html')

def mybooks(request):
    user=request.user.username
    data=models.My_users.objects.get(username=user)
    return render(request,'home.html',{'data':data,'flag':1})

def logout(request):
    auth.logout(request)
    return render(request,'index.html')



def login(request):
    if request.method=="POST":
        username=request.POST['Username']
        password=request.POST['Password']
        print(username,password)

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)

            #data=models.File.objects.filter(username=request.user.username)
            user=request.user.username
            data=models.My_users.objects.get(username=user)
            books=models.File.objects.filter(username=request.user.username)
            return render(request,'home.html',{'data':data,'books':books})
        else:
            print('not auth')
            messages.info(request,'*invalid credentails')
            return render(request,'index.html',{'data1':'1'})
    else:
        return render(request,'index.html')


def change(request):
    if request.method=="POST":
        password=request.POST['Password']
        password1=request.POST['ConfirmPassword']
        username=request.user.username
        u=User.objects.get(username=username)
        u.set_password(password)
        u.save()
        user=auth.authenticate(username=username,password=password)
        auth.login(request,user)
        data=models.My_users.objects.get(username=username)
        books=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data,'books':books})


def changepassword(request):
    if request.method=="POST":
        username=request.POST['uname']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        print(username)
        print(email)
        print(password)
        print(password1)
        u=User.objects.get(username__exact=username)
        u.set_password(password)
        u.save()
        return render(request,'index.html')
