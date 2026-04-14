import os
import random
from datetime import datetime


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group,User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from flatvue import settings
from myapp.models import *

def login_load(request):
    return render(request,"loginindex.html")

def logout(request):
    return render(request,"loginindex.html")



def login_post(request):
    print(request.POST,"kkkkkkkkkkkkkkk")
    uname=request.POST['Username']
    password=request.POST['password']

    ob=authenticate(request,username=uname,password=password)
    if ob is not None:
        print("lllllllll")
        if ob.groups.filter(name="admin").exists():
            print("hhhhhhhhhhhhhhhhhhhh")
            login(request,ob)
            return redirect('/myapp/adminhome/')
        elif ob.groups.filter(name="FlatOwner").exists():
            login(request,ob)
            return redirect('/myapp/flat_owner_home/')
        elif ob.groups.filter(name="service_provider").exists():
            login(request,ob)
            return redirect('/myapp/service_provider_home/')
        else:
            return redirect('/myapp/login_load/')
    return redirect('/myapp/login_load/')


# =========================================
def admin_verify_flat_owner(request):
    ab=flat_owner.objects.all()
    return render(request,"Admin/verify flat owner.html",{'data':ab})

def admin_approve_flat_owner(request,id):
    flat_owner.objects.filter(LOGIN=id).update(Status="Accepted")
    return redirect('/myapp/admin_verify_flat_owner/')

def admin_reject_flat_owner(request,id):
    flat_owner.objects.filter(LOGIN=id).update(Status="Rejected")
    return redirect('/myapp/admin_verify_flat_owner/')



def admin_view_app_review(request):
    ab=feedback_table.objects.all()
    return render(request,"Admin/view app review.html",{'data':ab})

def admin_view_facilities(request):
    ab=facilities_table.objects.all()
    return render(request,"Admin/view facilities.html",{'facilities':ab})

def admin_view_flat_details(request):
    ab=flat_table.objects.all()
    return render(request,"Admin/view flat details.html",{'data':ab})

def adminhome(request):
    return render(request,'Admin/adminindex.html')

def admin_changepassword(request):
    return render(request,'Admin/changepassword.html')

def changepass_post(request):
    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']

    f=check_password(current_password, request.user.password)
    if f:
        if new_password==confirm_password:
            user=request.user
            user.set_password(confirm_password)
            user.save()
            messages.success(request,"Password changed successfully. PLease log in again.")
            return redirect('/myapp/login_load/')
        else:
            messages.error(request,"New password and confirm password do not match.")
            return redirect('/myapp/admin_changepassword/')
    else:
        messages.error(request,"Current password is incorrect.")
        return redirect('/myapp/admin_changepassword/')



# =================================================================


def flat_owner_home(request):
    return render(request,"flat owner/index.html")

def flat_owner_add_broadcast_notification(request,id):
    request.session['nid']=id
    return render(request,"flat owner/add broadcast notification.html")


def addbrdcastnotif_post(request):
    date=request.POST['date']
    notification=request.POST['notification']
    details=request.POST['details']

    print(request.POST)

    ob=notification_table()
    ob.date=date
    ob.notification=notification
    ob.details=details
    ob.FLAT_id=request.session['nid']
    ob.save()
    return redirect('/myapp/flat_owner_view_flat/')



def flat_owner_add_flat_occupants(request):

    owner = flat_owner.objects.get(LOGIN=request.user)
    owner_flats = flat_table.objects.filter(FLAT_OWNER=owner)
    occupied_flats = flat_occupant.objects.values_list('FLAT_id', flat=True)
    available_flats = owner_flats.exclude(id__in=occupied_flats)
    return render(request, "flat owner/add flat occupants.html", {
        'data': available_flats
    })


def addflatoccu_post(request):
    print(request.FILES,"kkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    district=request.POST['district']
    proof=request.FILES['Proof']
    image=request.FILES['image']
    # owner=request.POST['owner']
    flat=request.POST['flat']
    username=request.POST['username']
    password=request.POST['password']



    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    fs2=FileSystemStorage()
    path2=fs2.save(proof.name,proof)



    obj=User.objects.create_user(username=username,password=password,first_name=name,email=email)
    obj.save()
    obj.groups.add(Group.objects.get(name='FlatOccupant'))

    ob=flat_occupant()
    ob.name=name
    ob.LOGIN=obj
    ob.contact=phone
    ob.photo=path
    ob.proof=path2
    ob.email=email
    ob.FLAT_id=flat
    ob.place=place
    ob.district=district
    ob.save()

    return redirect('/myapp/flat_owner_manage_flat_occu/')



def flat_owner_add_rent_or_payment(request):
    occupants = flat_occupant.objects.all()
    return render(request, "flat owner/add rent or payment.html", {"data": occupants})

def addrentorpaym_post(request):
    if request.method == "POST":
        occupant_id = request.POST['occupant']
        rent = request.POST['rent']
        duration = request.POST['duration']

        occ = flat_occupant.objects.get(id=occupant_id)
        if rent_table.objects.filter(FLAT_OCCUPANT=occ, status='pending').exists():
            return HttpResponse(
                "<script>alert('Occupant already has a pending rent entry');history.back();</script>"
            )
        a = rent_table()
        a.FLAT_OCCUPANT = occ
        a.rent = rent
        a.pending_rent = rent
        a.date = datetime.now()
        a.duration = duration
        a.status = 'pending'
        a.save()

        return redirect('/myapp/flat_owner_manage_rent/')


def flat_owner_add_security(request):
    return render(request,"flat owner/add security.html")

def addsecurity_post(request):
    print(request.user.id,"kkkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    image=request.FILES['image']
    proof=request.FILES['proof']

    fs = FileSystemStorage()
    path = fs.save(image.name,image)

    fs2 = FileSystemStorage()
    path2 = fs2.save(proof.name,proof)

    username=request.POST['username']
    password=request.POST['password']


    obj=User.objects.create_user(username=username,password=password,first_name=password,email=email)
    obj.save()
    obj.groups.add(Group.objects.get(name='Security'))

    ob=security_table()
    ob.name=name
    ob.LOGIN=obj
    ob.FLAT_OWNER=flat_owner.objects.get(LOGIN__id=request.user.id)
    ob.phone=phone
    ob.email=email
    ob.place=place
    ob.image=path
    ob.proof=path2
    ob.save()
    return redirect('/myapp/flat_owner_manage_security/')



def flat_owner_add_service_provider(request):
    return render(request,"flat owner/add service provider.html")

def adddservprovi_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    field=request.POST['field']
    proof=request.FILES['proof']
    fs=FileSystemStorage()
    fn=fs.save(proof.name,proof)
    image=request.FILES['image']
    fs1 = FileSystemStorage()
    fn1 = fs1.save(image.name, image)
    username=request.POST['username']
    password=request.POST['password']

    obj=User.objects.create(username=username,password=make_password(password),email=email)
    obj.save()
    obj.groups.add(Group.objects.get(name='service_provider'))

    ob=service_provider()
    ob.LOGIN=obj
    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.field=field
    ob.proof=fn
    ob.image=fn1
    ob.save()


    return redirect('/myapp/flat_owner_manage_service_provider/')



def flat_owner_add_surveillance_camera(request):
    return render(request,"flat owner/add surveillance camera.html")
def addsurvcamera_post(request):
    camerano=request.POST['camerano']
    details=request.POST['details']
    location=request.POST['location']
    owner = flat_owner.objects.get(LOGIN=request.user)

    ob=surveillance_camera()
    ob.camera_no=camerano
    ob.details=details
    ob.location=location
    ob.FLAT_OWNER = owner
    ob.save()
    return redirect('/myapp/flat_owner_manage_cam/')



def flat_owner_assign_service_provider(request):
    return render(request,"flat owner/assign service provider.html")

def flat_owner_assign_work(request,id):
    request.session['sqid']=id
    return render(request,"flat owner/assign work.html")


def assignwork_post(request):
    print(request.session['sqid'],"hhhhhhhhhhhhhhhhhh")
    work=request.POST['work_title']
    date=request.POST['date']
    ob=duty_to_security_table()
    ob.SECURITY=security_table.objects.get(id=request.session['sqid'])
    ob.work=work
    ob.date=date
    ob.Status='pending'
    ob.save()
    return redirect('/myapp/flat_owner_manage_security/')






def flat_owner_complaint_reply(request,id):
    request.session['cid']=id
    return render(request,"flat owner/complaint reply.html")
def flat_owner_complaint_reply_post(request):
    reply=request.POST['reply']
    obj=complaint_table.objects.get(id=request.session['cid'])
    obj.reply=reply
    obj.save()
    return redirect('/myapp/flat_owner_view_complaints/#about')


def flat_owner_edit_flat_occupants(request):
    return render(request,"flat owner/edit flat occupants.html")

def editflatoccu_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    district=request.POST['district']
    image = request.FILES['image']
    proof=request.FILES['proof']

    ob=flat_occupant()
    ob.name=name
    ob.contact=phone
    ob.photo=image
    ob.proof=proof
    ob.email=email
    ob.place=place
    ob.district=district
    ob.save()

    return redirect('/myapp/flat_owner_manage_flat_occu/')



def flat_owner_edit_security(request,id):
    request.session['sid']=id
    ob=security_table.objects.get(id=id)
    return render(request,"flat owner/edit security.html",{"data":ob})
def editsecurity_post(request):

    sid = request.session.get('sid')
    a = security_table.objects.get(id=sid)


    a.name = request.POST.get('name', a.name)
    a.email = request.POST.get('email', a.email)
    a.phone = request.POST.get('phone', a.phone)
    a.place = request.POST.get('place', a.place)

    if 'image' in request.FILES:
        a.image = request.FILES['image']

    if 'proof' in request.FILES:
        a.proof = request.FILES['proof']

    a.save()

    return redirect('/myapp/flat_owner_manage_security/')

def flat_owner_edit_service_provider(request,id):
    request.session['spid']=id
    ob=service_provider.objects.get(id=id)
    return render(request,"flat owner/edit service provider.html",{"data":ob})

def editservprovider_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    field=request.POST['field']


    ob = service_provider.objects.get(id=request.session['spid'])

    if "image" in request.FILES:
         image=request.FILES['image']
         ob.image = image
         ob.save()
    if "proof" in request.FILES:
         proof=request.FILES['image']
         ob.proof = proof
         ob.save()

    ob.name=name
    ob.email=email
    ob.phone=phone
    ob.place=place
    ob.field=field

    ob.save()

    return redirect('/myapp/flat_owner_manage_service_provider/')

def delete_security(request,id):
    security_table.objects.filter(LOGIN=id).delete()
    User.objects.filter(id=id).delete()
    return redirect('/myapp/flat_owner_manage_security/')

def flat_owner_delete_service_provi(request,id):
    ab=service_provider.objects.get(id=id)
    ab.delete()
    return redirect('/myapp/flat_owner_manage_service_provider/')



def flat_owner_edit_cam(request,id):
    camera = surveillance_camera.objects.get(id=id)
    request.session['cid']=id
    return render(request,"flat owner/edit surveillance camera.html",{"i":camera})
def editcamera_post(request):
    camerano=request.POST['camerano']
    details=request.POST['details']
    location=request.POST['location']

    ob=surveillance_camera.objects.get(id=request.session['cid'])
    ob.camera_no=camerano
    ob.details=details
    ob.location=location
    ob.save()
    return redirect('/myapp/flat_owner_manage_cam/')


def flat_owner_delete_camera(request,id):
    ob=surveillance_camera.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/flat_owner_manage_cam/')

def flat_owner_manage_bd_notif(request,id):
    ob=notification_table.objects.filter(FLAT_id=id)
    request.session['nid']=id
    return render(request,"flat owner/manage broadcast notification.html",{"data":ob})

def flat_owner_delete_bdnotif(request,id):
    ob=notification_table.objects.get(id=id)
    ob.delete()
    k=request.session['nid']
    return redirect(f'/myapp/flat_owner_manage_bd_notif/{k}')


def flat_owner_manage_flat_occu(request):
    abcd = flat_occupant.objects.filter(FLAT__FLAT_OWNER__LOGIN_id=request.user.id)
    return render(request,"flat owner/manage flat occupants.html", {'data': abcd})


def flat_owner_delet_flat_occupant(request,id):
    print(id,"jjjjjjjjjjjjjjjjjjjj")
    ob=flat_occupant.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/flat_owner_manage_flat_occu/')

def flat_owner_edit_flat_occupant(request,id):
    ab=flat_occupant.objects.get(id=id)
    request.session['eid']=id
    return render(request,"flat owner/edit flat occupants.html",{'data':ab})

def editflatoccupant_post(request):
    name=request.POST['name']
    contact=request.POST['phone']

    email=request.POST['email']
    place=request.POST['place']
    district=request.POST['district']
    ob=flat_occupant.objects.get(id=request.session['eid'])

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        ob.photo = photo
        ob.save()

    if 'proof' in request.FILES:
        proof = request.FILES['proof']
        ob.proof = proof
        ob.save()

    ob.name=name
    ob.contact=contact
    ob.email=email
    ob.place=place
    ob.district=district
    ob.save()
    return redirect('/myapp/flat_owner_manage_flat_occu/')

def flat_owner_manage_rent(request):
    ob=rent_table.objects.all()
    return render(request,"flat owner/manage rent or payment.html",{"data":ob})

def flat_owner_manage_security(request):
    ob=security_table.objects.all()
    print(ob,"kkkkkkkkkkkkkkkkkkkkkk")
    return render(request,"flat owner/manage security.html",{"data":ob})

def flat_owner_manage_service_provider(request):
    ob=service_provider.objects.all()
    return render(request,"flat owner/manage service provider.html",{"data":ob})

def flat_owner_manage_cam(request):
    ob=surveillance_camera.objects.all()
    return render(request,"flat owner/manage surveillance camera.html",{"data":ob})

def ViewSuspiciosActivity(request,id):
    ob=suspicious_activities.objects.filter(CAMERA__id=id)
    return render(request,'Flat Owner/view Suspicious Activity.html',{'data':ob})

def flat_owner_monitor_pay_status(request):
    return render(request,"flat owner/monitor payment status.html")

def flat_owner_add_flat(request):
    return render(request,"Flat Owner/add flat.html")


def addflat_post(request):
    price=request.POST['price']
    squarefeet=request.POST['squarefeet']
    rooms=request.POST['rooms']
    flatnumber=request.POST['flatnumber']
    floor=request.POST['floor']
    place=request.POST['place']

    latitude=request.POST['latitude']
    longitude=request.POST['longitude']
    ob=flat_table()
    ob.price=price
    ob.squarefeet=squarefeet
    ob.rooms=rooms
    ob.flatnumber=flatnumber
    ob.floor=floor
    ob.place=place
    ob.latitude=latitude
    ob.longitude=longitude
    ob.FLAT_OWNER=flat_owner.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return redirect('/myapp/flat_owner_view_flat/')

def flat_owner_view_flat(request):
    abcd=flat_table.objects.filter(FLAT_OWNER__LOGIN_id=request.user.id)
    return render(request,"flat owner/view flat.html",{'data':abcd})



def flat_owner_delet_flat(request,id):
    flat_table.objects.get(id=id).delete()
    return redirect('/myapp/flat_owner_view_flat/')


def flat_owner_edit_flat(request,id):
    ab=flat_table.objects.get(id=id)
    request.session['eid']=id
    return render(request,"flat owner/edit flat.html",{'data':ab})


def editflat_post(request):
    price=request.POST['price']
    squarefeet=request.POST['squarefeet']
    rooms=request.POST['rooms']
    flatnumber=request.POST['flatnumber']
    floor=request.POST['floor']
    place=request.POST['place']
    latitude=request.POST['latitude']
    longitude=request.POST['longitude']
    ob=flat_table.objects.get(id=request.session['eid'])
    ob.price=price
    ob.squarefeet=squarefeet
    ob.rooms=rooms
    ob.flatnumber=flatnumber
    ob.floor=floor
    ob.place=place
    ob.latitude=latitude
    ob.longitude=longitude
    ob.FLAT_OWNER=flat_owner.objects.get(LOGIN=request.user.id)
    ob.save()
    return redirect('/myapp/flat_owner_view_flat/')





def flat_owner_reg_flat_owner(request):
    return render(request,"flat owner/registration flat owner.html")
def regflatowner_post(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    proof=request.FILES['proof']
    image=request.FILES['image']
    username=request.POST['username']
    password=request.POST['password']

    owner_login=User.objects.create(username=username,password=make_password(password))
    owner_login.save()
    owner_login.groups.add(Group.objects.get(name="FlatOwner"))
    obj=flat_owner()
    obj.LOGIN=owner_login
    obj.name=name
    obj.email=email
    obj.phone=phone
    obj.place=place
    obj.proof=proof
    obj.image=image
    obj.Status='pending'
    obj.save()


    return redirect('/myapp/login_load/')



def flat_owner_service_req_reply(request):
    return render(request,"flat owner/service request reply.html")

def flat_owner_view_complaints(request):
    ab=complaint_table.objects.all()
    return render(request,"flat owner/view complaints.html",{"data":ab})

def flat_owner_view_service_req(request):
    ab=service_request_table.objects.all()
    return render(request,"flat owner/view service request.html",{"data":ab})

def flat_owner_view_spot_notif(request):

    ab = suspicious_activities.objects.filter(
        CAMERA__FLAT_OWNER__LOGIN_id=request.user.id
    )
    return render(request,"flat owner/view spot notification(from AI suveillance).html",{"data":ab})

def flat_owner_view_entry_exit_log(request):
    ab=visitor_entry_table.objects.all()
    return render(request,"flat owner/view visitor entry and exit logs.html",{"data":ab})


def flat_owner_add_facilities(request):
    return render(request,"flat owner/add facilities.html")

def addfacilities_post(request):
    name=request.POST['name']
    date=request.POST['date']
    details=request.POST['details']

    ob=facilities_table()
    ob.FLAT_OWNER=flat_owner.objects.get(LOGIN__id=request.user.id)
    ob.name=name
    ob.date=date
    ob.details=details
    ob.save()
    return redirect('/myapp/flat_owner_manage_facilities/')

def flat_owner_manage_facilities(request):
    ab=facilities_table.objects.all()
    return render(request,"flat owner/manage facilities.html",{'facilities':ab})


# =================================================================

def service_provider_home(request):
    return render(request, "service provider/index.html")


def service_provider_add_complaint(request):
    return render(request,"service provider/add complaint.html")
def addcomplaint_post(request):
    complaint=request.POST['complaint']


    ob=complaint_table()
    ob.LOGIN_id=request.user.id
    ob.date=datetime.today()
    ob.complaint=complaint
    ob.reply='pending'
    ob.save()
    return redirect('/myapp/service_provider_view_complaint/')



def service_provider_add_services(request):
    return render(request,"service provider/add services.html")
def addservices_post(request):
    service=request.POST['service']
    type=request.POST['type']
    field=request.POST['field']
    amount=request.POST['amount']

    ob=Service_table()
    ob.SERVICE_PROVIDER = service_provider.objects.get(LOGIN__id=request.user.id)
    ob.service=service
    ob.type=type
    ob.field=field
    ob.amount=amount
    ob.save()
    return redirect('/myapp/service_provider_manage_services/')



def service_provider_manage_ongoing_services(request):
    return render(request,"service provider/manage ongoing services.html")



def service_provider_manage_services(request):
    ob=Service_table.objects.all()
    return render(request,"service provider/manage services.html",{'data':ob})

def service_provider_update_ongoing_services(request):
    return render(request,"service provider/update ongoing services.html")

def service_provider_view_complaint(request):
    ob=complaint_table.objects.all()
    return render(request,"service provider/view complaint.html",{'data':ob})

def service_provider_view_service_req(request):
    ob=service_request_table.objects.all()
    return render(request,"service provider/view service requests.html",{'data':ob})

def service_provider_approve_servicerequest(request,id):
    service_request_table.objects.filter(id=id).update(status="Accepted")
    return redirect('/myapp/service_provider_view_service_req/')

def service_provider_reject_servicerequest(request,id):
    service_request_table.objects.filter(id=id).update(status="Rejected")
    return redirect('/myapp/service_provider_view_service_req/')


def service_provider_edit_services(request,id):
    service=Service_table.objects.get(id=id)
    request.session['sid']=id
    return render(request,"service provider/edit services.html",{"service":service})
def editservices_post(request):
    service=request.POST['service']
    type=request.POST['type']
    field=request.POST['field']
    amount=request.POST['amount']

    ob=Service_table.objects.get(id=request.session['sid'])
    ob.SERVICE_PROVIDER=service_provider.objects.get(LOGIN__id=request.user.id)
    ob.service=service
    ob.type=type
    ob.field=field
    ob.amount=amount
    ob.save()
    return redirect('/myapp/service_provider_manage_services/')

def service_provider_delete_services(request,id):
    Service_table.objects.filter(id=id).delete()
    return redirect('/myapp/service_provider_manage_services/')


# =================================================================
#


def LoginPostFlutter(request):
    username = request.POST.get("username")
    print(username,'aaaaaaaaaaa')
    password = request.POST.get("password")
    print(password,'bbbbbbbbbbbb')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.groups.filter(name="FlatOccupant").exists():
            login(request, user)
            print(User,'ppppppppppppppp')
            return JsonResponse({
                'status': 'ok',
                'lid': str(request.user.id),
                'type': 'FlatOccupant'
            })

        elif user.groups.filter(name="Security").exists():
            login(request, user)
            print(user,'sssssssssssssssssssssssss')
            return JsonResponse({
                'status': 'ok',
                'lid': str(user.id),
                'type': 'Security'
            })

        else:
            return JsonResponse({'status': 'no'})

    return JsonResponse({'status': 'no'})



def sendcomplaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    lob = complaint_table()
    lob.LOGIN =User.objects.get(id=lid)
    lob.complaint = complaint
    lob.date = datetime.today()
    lob.reply='pending'
    lob.save()
    return JsonResponse({'status': 'ok'})



def sendfeedback(request):
    comp = request.POST['feedback']
    rating=request.POST['rating']
    lid = request.POST['lid']
    lob = feedback_table()
    lob.OCCUPANT =flat_occupant.objects.get(LOGIN__id=lid)
    lob.feedback = comp
    lob.rating=rating
    lob.date = datetime.today()
    lob.save()
    return JsonResponse({'task': 'ok'})


def Add_visitor(request):
    name = request.POST['name']
    relation = request.POST['relation']
    no_of_persons = request.POST['no_of_persons']
    time_schedule = request.POST['time_schedule']
    lid = request.POST['lid']
    lob = visitor_entry_table()
    lob.Name = name
    lob.Relation = relation
    lob.No_of_persons = no_of_persons
    lob.entry_time=time_schedule
    lob.date=datetime.today()
    lob.OCCUPANT = flat_occupant.objects.get(LOGIN__id=lid)
    lob.Status='pending'
    lob.save()

    # Generate QR Code using saved ID
    import qrcode
    img = qrcode.make(str(lob.id))
    img_path = f"C:\\Users\\muham\\PycharmProjects\\flatvue\\media\\qrcode\\{lob.id}.png"
    img.save(img_path)

    # Save QR Code table
    obj = QR_Code()
    obj.qrcode = f'/media/qrcode/{lob.id}.png'
    obj.date = datetime.now()
    obj.VISITOR = lob  # ✅ directly assign
    obj.save()
    return JsonResponse({'status': 'ok'})


def Viewfeedback(request):
    user_id=request.POST['lid']
    l=[]
    ab=feedback_table.objects.filter(OCCUPANT__LOGIN_id=user_id)
    for i in ab:
        l.append({
            'id': str(i.id),
            'OCCUPANT': str(i.OCCUPANT.name),
            'feedback': str(i.feedback),
            'rating': str(i.rating),
            'date': str(i.date),
        })
    return JsonResponse({'status':'ok','data':l})


def viewreply(request):
    user_id=request.POST['lid']
    l=[]
    ab=complaint_table.objects.filter(LOGIN_id=user_id)
    for i in ab:
        l.append({
            'id':str(id),
            'complaint':str(i.complaint),
            'reply':str(i.reply),
            'date':str(i.date),

        })
    return JsonResponse({'status':'ok','data':l})


def viewduty(request):
    sid=request.POST['lid']
    l=[]
    ab=duty_to_security_table.objects.filter(SECURITY__LOGIN_id=sid)
    for i in ab:
        l.append({
            'id':str(id),
            'work':str(i.work),
            'date':str(i.date),
            'Status':str(i.Status),

        })
    return JsonResponse({'status':'ok','data':l})


def viewnotification(request):
    l=[]
    ab=duty_to_security_table.objects.all()
    for i in ab:
        l.append({
            'id':str(id),
            'notification':str(i.notification),
            'details':str(i.details),
            'date':str(i.date),
            'title':str(i.title),
            'OCCUPANT': str(i.FLAT_OCCUPANT.name),

        })
    return JsonResponse({'status':'ok','data':l})


from django.http import JsonResponse

def view_visitors(request):
    l = []
    lid = request.POST['lid']

    visitors = visitor_entry_table.objects.filter(
        OCCUPANT__LOGIN_id=lid
    ).prefetch_related('qr_code_set')

    for i in visitors:
        qr = i.qr_code_set.first()

        if qr and qr.qrcode:
            qr_url = str(qr.qrcode)
        else:
            qr_url = None

        l.append({
            'id': i.id,
            'name': i.Name,
            'noofperson': i.No_of_persons,
            'date': str(i.date),
            'entry_time': str(i.entry_time),
            'qrcode': qr_url
        })

    return JsonResponse({'status': 'ok', 'data': l})




#
# def view_visitors(request):
#     l = []
#     lid = request.POST['lid']
#     visitors = visitor_entry_table.objects.filter(OCCUPANT__LOGIN_id=lid)
#
#     for i in visitors:
#         qr = QR_Code.objects.filter(VISITOR_id=i.id).first()
#
#         l.append({
#             'id': str(i.id),
#             'name': str(i.Name),
#             'noofperson': str(i.No_of_persons),
#             'date': str(i.date),
#             'entry_time': str(i.entry_time),
#             'qrcode': qr.qrcode.replace("/media/","/media/")
#         })
#
#     return JsonResponse({'status': 'ok', 'data': l})


def view_notifications(request):
    l = []
    lid = request.POST['lid']

    f=flat_occupant.objects.get(LOGIN=lid).FLAT.id
    ab = notification_table.objects.filter(FLAT_id=f)
    for i in ab:
        l.append({
            'id': str(id),
            'notification': str(i.notification),
            'details': str(i.details),
            'date': str(i.date),

        })
    return JsonResponse({'status': 'ok', 'data': l})


def view_emergency_notification(request):
    lid=request.POST['lid']
    l=[]
    ab=emergency_notification_table.objects.exclude(FLAT_OCCUPANT__LOGIN_id=lid)
    for i in ab:
        l.append({
            'id':str(id),
            'notification':str(i.notification),
            'details':str(i.details),
            'date':str(i.date),
            'OCCUPANT': str(i.FLAT_OCCUPANT.name),

        })
    return JsonResponse({'status':'ok','data':l})


def send_emergency_notification(request):
    notification = request.POST['notification']
    details = request.POST['details']
    lid = request.POST['lid']
    ob=emergency_notification_table()
    ob.notification=notification
    ob.details=details
    ob.date=datetime.now().date()
    ob.FLAT_OCCUPANT=flat_occupant.objects.get(LOGIN=lid)
    ob.save()
    return JsonResponse({'status':'ok','data':1})



def viewservices(request):
    l = []
    # lid = request.POST['lid']
    ab = Service_table.objects.all()
    for i in ab:
        l.append({
            'id': str(i.id),
            'service': str(i.service),
            'type': str(i.type),
            'field': str(i.field),
            'amount': str(i.amount),

        })
    return JsonResponse({'status': 'ok', 'data': l})




def view_rent(request):
    lid=request.POST['lid']
    i=rent_table.objects.get(FLAT_OCCUPANT__LOGIN_id=lid)
    return JsonResponse({'status':'ok',
                         'id':str(i.id),
                        'pending_rent':str(i.pending_rent),
                        'rent':str(i.rent),
                        'date':str(i.date),
                        'duration':str(i.duration),
                        'rentstatus':str(i.status),})


def requestservices(request):
    request_field = request.POST['request_field']
    lid = request.POST['lid']
    sid=request.POST['sid']
    lob = service_request_table()
    lob.FLAT_OCCUPANT =flat_occupant.objects.get(LOGIN_id=lid)
    lob.SERVICE =Service_table.objects.get(id=sid)
    lob.request_field = request_field
    lob.date = datetime.today()
    lob.reply='pending'
    lob.status='pending'
    lob.save()
    return JsonResponse({'status': 'ok'})





def BookCommonArea(request):
    if request.method == 'POST':
        lid = request.POST.get('lid')
        area = request.POST.get('area')
        date = request.POST.get('date')

        try:
            occupant = flat_occupant.objects.get(LOGIN_id=lid)

            if book_common_area.objects.filter(area=area, date=date).exists():
                return JsonResponse({'status': 'already_booked'})

            book_common_area.objects.create(
                FLAT_OCCUPANT=occupant,
                area=area,
                date=date
            )

            return JsonResponse({'status': 'ok'})

        except flat_occupant.DoesNotExist:
            return JsonResponse({'status': 'invalid_user'})



def flatoccupant_viewprofile(request):
    lid=request.POST['lid']
    obj=flat_occupant.objects.get(LOGIN=lid)
    photo=request.build_absolute_uri(obj.photo.url)if obj.photo else""
    proof=request.build_absolute_uri(obj.proof.url)if obj.proof else""
    return JsonResponse({'status':'ok',
                         'name':obj.name,
                         'contact':obj.contact,
                         # 'proof':obj.photo,
                         'proof':proof,
                         'email':obj.email,
                         'place':obj.place,
                         'district':obj.district,
                         'photo': photo

                         })


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def change_password_flutter(request):
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    lid = request.POST.get('lid')

    try:
        user = User.objects.get(id=lid)
        if not check_password(current_password, user.password):
            return JsonResponse({'status': 'error', 'message': 'Current password is incorrect'})
        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'New passwords do not match'})
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Password changed successfully'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})




def monthly_rent_payment(request):
    rent_id = request.POST['rent_id']
    print(rent_id,"______________________________________________________")
    lid = request.POST['lid']
    amount = request.POST['amount']
    crn_date = datetime.now().date()

    ob = rent_table.objects.get(id=rent_id)
    pnd_amt = ob.pending_rent
    new_pnd_amt = float(pnd_amt) - float(float(amount)/100)
    ob.pending_rent = new_pnd_amt
    ob.save()

    month_name = crn_date.strftime("%B")

    ab = payment_table()
    ab.RENT = rent_table.objects.get(id=rent_id)
    ab.date = crn_date
    ab.Status = 'Paid'
    ab.month = month_name
    ab.save()
    return JsonResponse({"status": "ok"})




####################security#############################


def security_viewprofile(request):
    lid=request.POST['lid']
    obj=security_table.objects.get(LOGIN=lid)
    image=request.build_absolute_uri(obj.image.url)if obj.image else""
    proof=request.build_absolute_uri(obj.proof.url)if obj.proof else""
    return JsonResponse({'status':'ok',
                         'name':obj.name,
                         'phone':obj.phone,
                         # 'proof':obj.photo,
                         'proof':proof,
                         'email':obj.email,
                         'place':obj.place,
                         # 'district':obj.district,
                         'image': image

                         })


from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def security_view_notification(request):
    l = []
    lid = request.POST['lid']
    security = security_table.objects.get(LOGIN_id=lid)
    flats = flat_table.objects.filter(FLAT_OWNER=security.FLAT_OWNER)
    notifications = notification_table.objects.filter(FLAT__in=flats)

    for i in notifications:
        l.append({
            'id': i.id,
            'notification': i.notification,
            'details': i.details,
            'date': i.date.strftime("%Y-%m-%d"),
        })

    return JsonResponse({'status': 'ok', 'data': l})



def security_view_suspiciousactivity(request):
    l = []
    lid = request.POST['lid']

    security = security_table.objects.get(LOGIN_id=lid)

    notifications = suspicious_activities.objects.filter(
        CAMERA__FLAT_OWNER=security.FLAT_OWNER
    )

    for i in notifications:
        l.append({
            'id': i.id,
            'camera': i.CAMERA.camera_no,
            'location': i.CAMERA.location,
            'image': request.build_absolute_uri(i.image.url) if i.image else "",
            'date': i.date.strftime("%Y-%m-%d"),
        })

    return JsonResponse({'status': 'ok', 'data': l})





def security_change_password(request):
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    lid = request.POST.get('lid')  # Pass the user ID from Flutter

    try:
        user = User.objects.get(id=lid)

        # 1. Check if current password is correct
        if not check_password(current_password, user.password):
            return JsonResponse({'status': 'error', 'message': 'Current password is incorrect'})

        # 2. Check if new passwords match
        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'New passwords do not match'})

        # 3. Success: Update password
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Password changed successfully'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})



def viewdutyschedule(request):
    l = []
    lid = request.POST['lid']

    ab= duty_to_security_table.objects.filter(SECURITY__LOGIN_id=lid)
    for i in ab:
        l.append({
            'id': str(i.id),
            'work': str(i.work),
            'date': str(i.date),
            'status': str(i.Status),

        })
    return JsonResponse({'status': 'ok', 'data': l})

def update_status(request):
    wid = int(request.POST['wid'])  # 👈 force integer
    c = duty_to_security_table.objects.get(id=wid)
    c.Status = "Completed"
    c.save()
    return JsonResponse({'status': 'ok'})


def security_view_visitor(request):
    l = []
    lid = request.POST['lid']
    security = security_table.objects.get(LOGIN_id=lid)

    flats = flat_occupant.objects.filter(FLAT__FLAT_OWNER=security.FLAT_OWNER)
    v = visitor_entry_table.objects.filter(OCCUPANT__in=flats)

    for i in v:
        l.append({
            'id': i.id,
            'Name': i.Name,
            'Relation': i.Relation,
            'No_of_persons': i.No_of_persons,
            'entry_time': i.entry_time,
            'date': i.date.strftime("%Y-%m-%d"),
        })

    return JsonResponse({'status': 'ok', 'data': l})


def send_service_request(request):
    sid=request.POST['sid']
    lid=request.POST['lid']
    obj=service_request_table()
    obj.FLAT_OCCUPANT=flat_occupant.objects.get(LOGIN=lid)
    obj.SERVICE_id=sid
    obj.date=datetime.now().today()
    obj.status="pending"
    obj.save()
    return JsonResponse({'status':'ok'})








#
#
#
# #############Main
# import os
import cv2
import numpy as np
# from django.http import JsonResponse
# from django.core.files.base import ContentFile
# from django.utils import timezone
#
# # FIX: Set this before importing DeepFace to prevent Keras 3 errors
# os.environ["TF_USE_LEGACY_KERAS"] = "1"
from deepface import DeepFace

# from .models import flat_owner, flat_occupant, surveillance_camera, suspicious_activities
#
#
def check_stranger_api(request):
    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]
        camera_id = 1  # Hardcoded camera ID as requested

        try:
            # 1. Identify the camera and the owner it belongs to
            cam_obj = surveillance_camera.objects.get(id=camera_id)
            owner = cam_obj.FLAT_OWNER

            # 2. Convert uploaded bytes to OpenCV frame
            nparr = np.frombuffer(img_file.read(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 3. Gather all "Authorized" residents for this owner's ecosystem
            # We check the Owner themselves
            authorized_list = []
            if owner.image:
                authorized_list.append({'name': owner.name, 'path': owner.image.path})

            # We check all occupants linked to any flat owned by this owner
            occupants = flat_occupant.objects.filter(FLAT__FLAT_OWNER=owner).exclude(photo="")
            for occ in occupants:
                authorized_list.append({'name': occ.name, 'path': occ.photo.path})

            is_identified = False
            identified_name = ""

            # 4. AI Verification Loop
            for person in authorized_list:
                if not os.path.exists(person['path']):
                    continue

                try:
                    result = DeepFace.verify(
                        img1_path=frame,
                        img2_path=person['path'],
                        model_name="VGG-Face",
                        detector_backend="opencv",
                        enforce_detection=False
                    )

                    if result["verified"]:
                        is_identified = True
                        identified_name = person['name']
                        break
                except Exception:
                    continue

            # 5. Result Handling
            if not is_identified:
                # Save the frame as an Intruder image
                _, buffer = cv2.imencode('.jpg', frame)
                filename = f"intruder_{camera_id}_{timezone.now().strftime('%H%M%S')}.jpg"
                content = ContentFile(buffer.tobytes(), name=filename)

                # Log to suspicious_activities table
                log = suspicious_activities.objects.create(
                    CAMERA=cam_obj,
                    image=content,
                    date=timezone.now().date()
                )

                return JsonResponse({
                    "status": "stranger",
                    "message": "Suspicious activity logged",
                    "log_id": log.id
                })

            return JsonResponse({
                "status": "authorized",
                "name": identified_name
            })

        except surveillance_camera.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Camera not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

#
#
# ##############


from django.http import JsonResponse
from django.utils import timezone
from .models import visitor_entry_table, QR_Code


def mark_visitor(request):
    if request.method == "POST":

        qr = request.POST.get("qrcode")

        if not qr:
            return JsonResponse({"message": "No QR code received"})

        today = timezone.now().date()
        now_time = timezone.now().time()

        try:
            # Get QR record
            qr_obj = QR_Code.objects.get(id=qr)

            # Get visitor
            visitor = qr_obj.VISITOR

        except QR_Code.DoesNotExist:
            return JsonResponse({"message": "Invalid QR Code"})

        # Reset only if new day
        if visitor.date == today:
            visitor.date = today
            visitor.entry_time = None
            visitor.exit_time = None

        # ✅ FIRST SCAN → ENTRY
        if visitor.entry_time is not None:
            visitor.entry_time = datetime.now().time()
            visitor.Status = "Entered"
            visitor.save()

            return JsonResponse({
                "message": f"Entry marked for {visitor.Name}"
            })

        # ✅ SECOND SCAN → EXIT
        elif visitor.exit_time is None:
            visitor.exit_time = now_time
            visitor.Status = "Exited"
            visitor.save()

            return JsonResponse({
                "message": f"Exit marked for {visitor.Name}"
            })

        # ✅ THIRD SCAN
        else:
            return JsonResponse({
                "message": "Already exited today"
            })

    return JsonResponse({"message": "Invalid Request"})


#############################################################

def forgotpasswordflutter(request):
    email = request.POST.get('email')

    try:
        user = User.objects.get(email=email)
    except flat_occupant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    otp = random.randint(100000, 999999)
    PasswordResetOTP.objects.create(email=email, otp=otp)

    send_mail(
        'Your Verification Code',
        f'Your verification code is {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

    return JsonResponse({'status': 'ok', 'message': 'OTP sent'})


def verifyOtpflutterPost(request):
    email = request.POST['email']
    entered_otp=request.POST['entered_otp']
    otp_obj = PasswordResetOTP.objects.filter(email=email).latest('created_at')
    if otp_obj.otp == entered_otp:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})

def changePasswordflutter(request):
    email = request.POST['email']
    newpassword = request.POST['newPassword']
    confirmPassword = request.POST['confirmPassword']
    if newpassword == confirmPassword:
        try:
            user = User.objects.get(email=email)
            user.set_password(confirmPassword)
            user.save()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})



##########

def forgot_password(request):
    return render(request,'forgot/forgot.html')


def forgotPassword_otp(request):
    email=request.POST['email']
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/myapp/')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/myapp/verifyOtp/')

def verifyOtp(request):
    return render(request,'forgot/otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/myapp/new_password/')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/myapp/changePassword/')

def new_password(request):
    return render(request,'forgot/new_password.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.get(email=email)
        user.set_password(confirmPassword)
        user.save()
        messages.success(request, 'Password Updated Successfully')
        return redirect('/myapp/login_load/')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/myapp/new_password/')


def detect_noti(request):
    img=request.FILES['image']
    cam_id=request.POST['cam_id']
    ob=suspicious_activities()
    ob.CAMERA=surveillance_camera.objects.get(id=cam_id)
    ob.image=img
    ob.date=datetime.today()
    ob.save()
    return  JsonResponse({"task":"ok"})

def send_noti(request):
    try:
        pending=suspicious_activities.objects.filter(status='notification').first()
        if pending == None:
            return JsonResponse({'status':'no'})

        suspicious_activities.objects.filter(id=pending.id).update(status='send')

        msg=('Violence detected at camera number'+str(pending.CAMERA.camera_no)+','+str(pending.CAMERA.location)+', date : '+str(pending.date))

        return JsonResponse({'status':'ok','msg':msg})

    except Exception as e :
        print(e)
        return JsonResponse({'error':str(e)})



