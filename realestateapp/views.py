from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def landowner_register(request):
    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        license_no=request.POST['license']
        password=request.POST['password']
        if Login.objects.filter(username=email).exists():
            print("user already exists")
            messages.info(request,"Already Exist")
        else:
            if Landowner.objects.filter(email=email,phone=phone,license_no=license_no).exists():
                print("user already exists")
                messages.info(request,"Already Exist")
            else:
                q=Login.objects.create_user(username=email,usertype='owner',password=password,viewpassword=password,is_active=0)
                q.save()
                regqry=Landowner.objects.create(name=name,email=email,address=address,phone=phone,license_no=license_no,user=q)
                regqry.save()
                messages.info(request,"Registration completed successfully")
        return redirect('/login')       
    return render(request,'register_owner.html')

def user_register(request):
    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        aadhaar_no=request.POST['aadhaar']
        password=request.POST['password']
        if Login.objects.filter(username=email).exists():
            print("user already exists")
            messages.info(request,"Already Exist")
        else:
            if User.objects.filter(email=email,phone=phone,aadhaar_no=aadhaar_no).exists():
                print("user already exists")
                messages.info(request,"Already Exist")
            else:
                q=Login.objects.create_user(username=email,usertype='user',password=password,viewpassword=password)
                q.save()
                regqry=User.objects.create(name=name,email=email,address=address,phone=phone,aadhaar_no=aadhaar_no,user=q)
                regqry.save()
                messages.info(request,"Registration completed successfully")
        return redirect('/login')       
    return render(request,'register_user.html')

def login(request):
    if request.POST:
        username=request.POST['Email']
        Password=request.POST['Password']
        print(username,'##',Password)
        user=authenticate(username=username,password=Password)
        print(user)
        if user is not None:
            if user.usertype=='admin':
                id=user.id
                request.session['uid']=id
                messages.info(request,"login successfully")
                return redirect('/adminHome')
            elif user.usertype=='owner':
                id=user.id
                request.session['uid']=id
                messages.info(request,"login successfully")
                return redirect('/ownerHome')
            elif user.usertype=='user':
                id=user.id
                request.session['uid']=id
                messages.info(request,"login successfully")
                return redirect('/userHome')
            else:
                messages.info(request,"username or password invalid")
        else:
            messages.info(request,"username or password invalid")
    return render(request,'login.html')

    
############################## ADMIN  #######################

def adminHome(request):
    return render(request,'Admin/adminHome.html')

def view_landowner(request):
    qy=Landowner.objects.all() 
    return render(request,'Admin/landowner.html',{'qy':qy})

def view_users(request):
    qy=User.objects.all()
    return render(request,'Admin/users.html',{'qy':qy})

def approve_owners(request):
    status=request.GET['status']
    id=request.GET['id']
    owner=Login.objects.get(id=id)
    owner.is_active=int(status)
    owner.save()
    if status == '1':
        messages.info(request,"Land owner Approved successfully")
    else:
        messages.info(request,"Land owner Rejected successfully")
    return redirect('/viewowners')
    
def viewBookings_admin(request):
    qy=Booking.objects.all()
    return render(request,'Admin/viewbooking_admin.html',{'qy':qy})

def viewland_admin(request):
    qy=Landarea.objects.all
    return render(request,'Admin/viewland_admin.html',{'qy':qy})

def viewdetail_admin(request):
    id=request.GET.get('id')
    qy=Landarea.objects.get(id=id)
    return render(request,'Admin/viewdetail_admin.html',{'qy':qy})



################################   LANDOWNER   ############################

def ownerHome(request):
    return render(request,'Owner/ownerHome.html')

def addlandarea(request):
    uid=request.session['uid']
    if request.POST:
        location=request.POST['location']
        image=request.FILES.get('image')
        sqft=request.POST['sqft']
        price=request.POST['price']
        description=request.POST['description']
        owner=Landowner.objects.get(user=uid)
        existing_land = Landarea.objects.filter(location=location, description=description,sqft=sqft, owner=owner).first()
        if existing_land:
            messages.error(request, "Land area with the same location already exists.")
        else:
            land = Landarea.objects.create(location=location, image=image, description=description, owner=owner, sqft=sqft, price=price)
            land.save()
            messages.success(request, "Land area added successfully.")
        return redirect('/viewlandarea')
    return render(request,'Owner/addlandarea.html')

def viewlandarea(request):
    uid=request.session['uid']
    qy=Landarea.objects.filter(owner__user=uid)
    return render(request,'Owner/viewlandarea.html',{'qy':qy})

def viewareadetail(request):
    id=request.GET.get('id')
    qy=Landarea.objects.get(id=id)
    return render(request,'Owner/viewdetail.html',{'qy':qy})

def editlanddetail(request):
    id=request.GET.get('id')
    qy=Landarea.objects.get(id=id)
    if request.POST:
        status=request.POST['Status']
        price=request.POST['price']
        image=request.FILES.get('image')
        description=request.POST['description']
        qry=Landarea.objects.get(id=id)
        qry.status=status
        qry.description=description
        qry.price=price
        qry.image=image
        qry.save()
        messages.info(request,"Updated successfully")
        return redirect('/viewlandarea')
    return render(request,'Owner/editlanddetail.html',{'qy':qy})

def deleteland(request):
    id=request.GET.get('id')
    Landarea.objects.filter(id=id).delete()
    messages.info(request,"Deleted Successfully")
    return redirect('/viewlandarea')

def viewbookings_owner(request):
    uid=request.session['uid']
    qy=Booking.objects.filter(land__owner__user=uid)
    return render(request,'Owner/viewbookings.html',{'qy':qy})

def approvebooking(request):
    id=request.GET.get('id')
    Booking.objects.filter(id=id).update(status='Approved')
    messages.info(request,"Approved")
    return redirect('/viewbooking_owner')

def rejectbooking(request):
    id=request.GET.get('id')
    Booking.objects.filter(id=id).update(status='Rejected')
    messages.info(request,"Rejected")
    return redirect('/viewbooking_owner')   

################################   USERS  #############################

def userHome(request):
    return render(request,'User/userHome.html')

def viewland(request):
    qy=Landarea.objects.all()
    search_query = request.GET.get('search', '')
    qy = Landarea.objects.filter(
        Q(location__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(sqft__icontains=search_query)
    )
    return render(request,'User/viewland.html',{'qy':qy})

def viewdetail_user(request):
    id=request.GET.get('id')
    qy=Landarea.objects.get(id=id)
    return render(request,'User/viewdetail_user.html',{'qy':qy})

def bookland(request):
    uid=request.session['uid']
    id=request.GET.get('id')
    land=Landarea.objects.get(id=id)
    price=land.price
    user=User.objects.get(user=uid)
    advance=(price*10)/100
    if Booking.objects.filter(land=land,status='Booked').exists():
        msg = "The Land is not available"
        messages.info(request, msg)
        
    else:
        book=Booking.objects.create(price=price,land=land,user=user,advance=advance)
        book.save()
        messages.info(request,"Booked successfully")
    return redirect('/viewland_user')

def viewbooking(request):
    uid=request.session['uid']
    qy=Booking.objects.filter(user__user=uid)
    return render(request,'User/bookland.html',{'qy':qy})

def cancelbooking(request):
    id=request.GET.get('id')
    qy=Booking.objects.filter(id=id).update(status='Canceled')
    messages.info(request,"Cancel the land Booking")
    return redirect('/bookingdetail')

def advancepayment(request):
    id=request.GET.get('id')
    if request.POST:
        qry=Booking.objects.get(id=id)
        qry.status='paid'  
        qry.save()
        land=qry.land.id
        qy=Landarea.objects.filter(id=land).update(status='Not Available')
        messages.info(request,"Paid successfully")
        return redirect('/bookingdetail')
    return render(request,'User/payment.html')

from django.shortcuts import render
import pandas as pd
import pickle
import numpy as np

def house_price_predictor(request):
    data = pd.read_csv("cleaned_housedata.csv")
    pipe = pickle.load(open("RidgeModel.pkl", "rb"))

    prediction = None

    if request.method == 'POST':
        location = request.POST.get('location')
        bhk = int(request.POST.get('bhk'))
        bath = int(request.POST.get('bath'))
        sqft = float(request.POST.get('sqft'))

        input_data = pd.DataFrame([[location, sqft, float(bath), bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])
        prediction = np.round((pipe.predict(input_data)[0] * 1e5), 2)

    # Render the form with the prediction result
    locations = sorted(data['location'].unique())
    bhk_opt = [1, 2, 3, 4, 5, 6]
    bath_opt = [1, 2, 3, 4, 5, 6]
    context = {'locations': locations, 'bhk_opt': bhk_opt, 'bath_opt': bath_opt, 'prediction': prediction}
    return render(request, 'User/house_predictor.html', context)

