from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse  
from fileuploader.functions.functions import handle_uploaded_file  
from fileuploader.form import StudentForm
from django.contrib import messages

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def home(request):
	return render(request,'home.html')

def signup(request):
	if request.method == "POST":
		full_name=request.POST["full_name"]
		username=request.POST["username"]
		email=request.POST["email"]
		password=request.POST["password"]

		first_name=full_name.split()[0]
		last_name=" ".join(full_name.split()[1:])

		user = User.objects.create_user(first_name=first_name,
										last_name=last_name,
										username=username,
										email=email,
										password=password)

		owner_profile=OwnerProfile.objects.create(user=user)

		login(request,user)
		return redirect("/dashboard/")			
	return render(request,"signup.html")

def signin(request):
	if request.method == "POST":
		username=request.POST["username"]
		password=request.POST["password"]

		user=authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return redirect("/dashboard/")

	return render(request,"signin.html")

def dashboard(request):
	return render(request,"dashboard.html")

def instant_quote(request):
	return render(request,"upload_page.html")

def index(request):  
	if request.method == 'POST':  
		student = StudentForm(request.POST, request.FILES)  
		if student.is_valid():  
			handle_uploaded_file(request.FILES['file'])
			messages.info(request, 'Your password has been changed successfully!')
			return redirect('/index/')
	else:  
		student = StudentForm()  
		return render(request,"upload_page.html",{'form':student})  
