from django.shortcuts import render
from core import models
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.db.models import Q
import boto3
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    data=models.My_users.objects.get(username=request.user.username)
    books=models.File.objects.filter(username=request.user.username)
    return render(request,'home.html',{'data':data,'books':books,'book':1})



def upload(request):

    if request.method=="POST":
        uploadfile=request.FILES['document']
        log=request.user.username
        bookname=request.POST['book']
        b=bookname+log




        if  models.File.objects.filter(filename=b).exists():
                messages.info(request,'*book name is already available in your repository')
                books=models.File.objects.filter(username=request.user.username)

                username=request.user.username
                data=models.My_users.objects.get(username=username)
                flag=1
                print('not uploaded')
                return render(request,'home.html',{'data':data,'flag':flag})
        print('uploading........')


        client=boto3.client('s3')
        email= User.objects.get(username=log)
        email=email.email
        s=email
        data=uploadfile.read()
        s=s.replace('.','d')
        s=s.replace('@','a')
        u=log.replace(' ','s')
        bucket_name=log+'kumar'+s
        bucket_name=bucket_name.lower()
        print(bucket_name)
        res=client.put_object(ACL='public-read',Body=data,Bucket=bucket_name,Key=bookname)
        print('************************')
        print('object has been uploaded')
        url="https://"+bucket_name+".s3.ap-south-1.amazonaws.com/"+bookname
        print(url)
        data=models.File(username=log,filename=bookname+log,filename_real=bookname,url=url)
        data.save()





        books=models.File.objects.filter(username=request.user.username)
        print(type(uploadfile))


        print('uploaded')

        username=request.user.username
        data=models.My_users.objects.get(username=username)
        print(books)
        return render(request,'home.html',{'data':data,'books':books})




def delete(request):
    if request.method=="POST":
        filename_real=request.POST['filename1']
        log=request.user.username
        filename=filename_real+log
        print(filename)

        data=models.Backup(username=log,filename=filename,filename_real=filename_real,url='')
        data.save()
        data=models.File.objects.get(filename=filename).delete()
        username=request.user.username
        data=models.My_users.objects.get(username=username)
        books=models.File.objects.filter(username=request.user.username)
        print('deleted.....')
        return render(request,'home.html',{'data':data,'books':books,'book':1})


def share(request):

    filename_real=request.POST['sharefile']
    username=request.user.username
    print(filename_real)
    print(username)
    data=models.My_users.objects.get(username=username)
    books=models.File.objects.filter(username=request.user.username)
    return render(request,'home.html',{'data':data,'books':books,'fl':1,'file':filename_real})


def sharefile(request):
    if request.method=="POST":
        sharefile=request.POST['sendingfile']
        username=request.POST['usname']

        if User.objects.filter(username=username).exists():

            print('......shared....')
            log=request.user.username
            filename=sharefile
            email= User.objects.get(username=log)
            remail=User.objects.get(username=username)
            remail=remail.email
            email=email.email
            s=email
            s=s.replace('.','d')
            s=s.replace('@','a')
            u=log.replace(' ','s')
            bucket_name=u+'kumar'+s
            bucket_name=bucket_name.lower()
            sender_name=log
            receiver_name=username
            shared_filename=sharefile
            sender_email=email
            receiver_email=remail

            print(bucket_name)
            print(sender_name)
            print(receiver_name)
            print(shared_filename)
            print(sender_email)
            print(receiver_email)
            l=[sender_name,receiver_name,bucket_name,sender_email,receiver_email,shared_filename]
            print(l)
            url="https://"+bucket_name+".s3.ap-south-1.amazonaws.com/"+shared_filename
            print(url)
            store=models.SharedFiles(sender_name=sender_name,receiver_name=receiver_name,bucket_name=bucket_name,sender_email=sender_email,receiver_email=receiver_email,shared_filename=shared_filename,real_filename= url )
            store.save()
            data=models.My_users.objects.get(username=request.user.username)
            books=models.File.objects.filter(username=request.user.username)
            return render(request,'home.html',{'data':data,'books':books})
        else:
            print('.....invalid...')
            data=models.My_users.objects.get(username=request.user.username)
            books=models.File.objects.filter(username=request.user.username)
            messages.info(request,'Given username is does not exists')
            return render(request,'home.html',{'data':data,'books':books,'fl':1,'file':sharefile})



def sharedbooks(request):
    data=models.My_users.objects.get(username=request.user.username)
    sharedbooks=models.SharedFiles.objects.filter(sender_name=request.user.username)
    print(sharedbooks)
    if sharedbooks:
        return render(request,'home.html',{'data':data,'sharedbooks':sharedbooks,'shared':1,'share':1})
    else:
        return render(request,'home.html',{'data':data,'sharedbooks':sharedbooks,'shared':1,'share':1,'sno':1})



def receivedbooks(request):
    username=request.user.username
    receivedbooks=models.SharedFiles.objects.filter(receiver_name=username)
    data=models.My_users.objects.get(username=request.user.username)
    if receivedbooks:
        return render(request,'home.html',{'receivedbooks':receivedbooks,'data':data,'shared':1,'received':1})

    else:
        return render(request,'home.html',{'receivedbooks':receivedbooks,'data':data,'shared':1,'received':1,'rno':1})


def mybookssearch(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        data=models.My_users.objects.get(username=request.user.username)
        books= models.File.objects.filter(Q(filename_real=pattern) & Q(username=request.user.username))
        if len(books):
            return render(request,'home.html',{'books':books,'data':data,'book':1})
        else:
            return render(request,'home.html',{'data':data,'book':1})




def sharedbookssearch(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        data=models.My_users.objects.get(username=request.user.username)
        sharedbooks= models.SharedFiles.objects.filter(Q(shared_filename=pattern) & Q(sender_name=request.user.username))
        if len(sharedbooks):
            return render(request,'home.html',{'sharedbooks':sharedbooks,'data':data,'shared':1,'share':1})
        else:
            return render(request,'home.html',{'data':data,'shared':1,'share':1})




def receivedbookssearch(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        data=models.My_users.objects.get(username=request.user.username)
        receivedbooks= models.SharedFiles.objects.filter(Q(shared_filename=pattern) & Q(receiver_name=request.user.username))
        if len(receivedbooks):
            return render(request,'home.html',{'receivedbooks':receivedbooks,'data':data,'received':1,'shared':1})
        else:
            return render(request,'home.html',{'data':data,'received':1,'shared':1})



def stopsharing(request):
    current_user=request.user.username
    receiver=request.POST['receiver']
    filename=request.POST['filename']
    data=models.SharedFiles.objects.filter(Q(sender_name=current_user) & Q(receiver_name=receiver) & Q(shared_filename=filename)).delete()
    data=models.My_users.objects.get(username=request.user.username)
    sharedbooks=models.SharedFiles.objects.filter(sender_name=request.user.username)
    print(sharedbooks)
    return render(request,'home.html',{'data':data,'sharedbooks':sharedbooks,'shared':1,'share':1})





def removereceiving(request):
    file=request.POST['filename1']
    user=request.user.username
    data=models.SharedFiles.objects.filter(Q(receiver_name=user) & Q(shared_filename=file)).delete()
    receivedbooks=models.SharedFiles.objects.filter(receiver_name=request.user.username)
    data=models.My_users.objects.get(username=request.user.username)
    return render(request,'home.html',{'receivedbooks':receivedbooks,'data':data,'shared':1,'received':1})


def reset(request):
    return render(request,'reset.html',{'password':1})


l=[]

def sendemail(request):
    email=request.POST['email']
    if User.objects.filter(email=email).exists():
       username=User.objects.get(email=email)
       username=username.username
       OTP=get_random_string(length=6, allowed_chars='1234567890')
       html_content=OTP
       l.clear()
       l.append(str(OTP))
       print("****************************")
       print(l)
       print(html_content)
       print(username)
       print(email)
       #send_mail('OTP for mycloudbooks account password reset',html_content, settings.EMAIL_HOST_USER,[email],fail_silently=False)
       return render(request,'reset.html',{'uname':username,'email':email,'otp':1})
    else:
       messages.info(request,'*invalid email')
       l.clear()
       return render(request,'reset.html',{'password':1})



def check(request):
    otp=str(request.POST['otp'])
    uname=request.POST['username']
    email=request.POST['email']
    temp=str(l[0])
    if temp==otp:
        
        print(email)
        print(uname)
        return render(request,'reset.html',{'uname':uname,'email':email,'reset':1})
    else:
        messages.info(request,'*invalid OTP')
        return render(request,'reset.html',{'uname':uname,'email':email,'otp':1})
