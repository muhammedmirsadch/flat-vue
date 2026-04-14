from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class  flat_owner(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=100)
    proof=models.FileField()
    image=models.FileField()
    Status=models.CharField(max_length=100)


class flat_table(models.Model):
    price=models.BigIntegerField()
    squarefeet=models.BigIntegerField()
    rooms=models.BigIntegerField()
    flatnumber=models.BigIntegerField()
    floor=models.BigIntegerField()
    place=models.CharField(max_length=100)
    FLAT_OWNER=models.ForeignKey(flat_owner,on_delete=models.CASCADE)
    longitude=models.FloatField()
    latitude=models.FloatField()

class service_provider(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    proof=models.FileField()
    image=models.FileField()
    place=models.CharField(max_length=100)
    field=models.CharField(max_length=100)

class Service_table(models.Model):
    SERVICE_PROVIDER=models.ForeignKey(service_provider,on_delete=models.CASCADE)
    service=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    field=models.CharField(max_length=100)
    amount=models.FloatField()


class flat_occupant(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    # OWNER=models.ForeignKey(flat_owner,on_delete=models.CASCADE)
    FLAT=models.ForeignKey(flat_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    contact=models.BigIntegerField()
    photo=models.FileField()
    proof=models.FileField()
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    district=models.CharField(max_length=100)



class complaint_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    date=models.DateField()



class rent_table(models.Model):
    FLAT_OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)
    rent=models.BigIntegerField()
    pending_rent=models.BigIntegerField()
    date=models.DateField()
    duration=models.CharField(max_length=100)
    status=models.CharField(max_length=100)





class notification_table(models.Model):
    notification=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    title=models.CharField(max_length=100)
    FLAT=models.ForeignKey(flat_table,on_delete=models.CASCADE)




class service_request_table(models.Model):
    FLAT_OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)
    SERVICE=models.ForeignKey(Service_table,on_delete=models.CASCADE)
    request_field=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)




class assign_service_provider(models.Model):
    SERVICE_REQUEST=models.ForeignKey(service_request_table,on_delete=models.CASCADE)
    SERVICE_PROVIDER=models.ForeignKey(service_provider,on_delete=models.CASCADE)
    date=models.DateField()
    Status=models.CharField(max_length=100)





class surveillance_camera(models.Model):
    camera_no=models.CharField(max_length=100)
    FLAT_OWNER=models.ForeignKey(flat_owner,on_delete=models.CASCADE)
    details=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='notification')




class payment_table(models.Model):
    month=models.CharField(max_length=100)
    RENT=models.ForeignKey(rent_table,on_delete=models.CASCADE)
    date=models.DateField()
    Status=models.CharField(max_length=100)





class feedback_table(models.Model):
    rating=models.FloatField()
    OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    date=models.DateField()





# class visitor_entry_table(models.Model):
#     Name=models.CharField(max_length=50)
#     Relation=models.CharField(max_length=50)
#     exit_time=models.CharField(max_length=50,default='pending')
#     No_of_persons=models.IntegerField()
#     entry_time=models.TimeField()
#     date=models.DateField()
#     OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)
#     Status=models.CharField(max_length=50)

class visitor_entry_table(models.Model):
    Name = models.CharField(max_length=50)
    Relation = models.CharField(max_length=50)
    No_of_persons = models.IntegerField()

    date = models.DateField()
    entry_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)

    OCCUPANT = models.ForeignKey('flat_occupant', on_delete=models.CASCADE)

    Status = models.CharField(max_length=50, default="pending")

class QR_Code(models.Model):
    qrcode = models.ImageField(upload_to='qrcode/')
    date=models.DateField()
    VISITOR=models.ForeignKey(visitor_entry_table,on_delete=models.CASCADE)



class security_table(models.Model):
    FLAT_OWNER=models.ForeignKey(flat_owner,on_delete=models.CASCADE)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    image=models.FileField()
    proof=models.FileField()



class duty_to_security_table(models.Model):
    SECURITY=models.ForeignKey(security_table,on_delete=models.CASCADE)
    work=models.CharField(max_length=100)
    date=models.DateField()
    Status=models.CharField(max_length=100)



class facilities_table(models.Model):
    name=models.CharField(max_length=100)
    FLAT_OWNER=models.ForeignKey(flat_owner,on_delete=models.CASCADE)
    date=models.DateField()
    details=models.CharField(max_length=100)



class emergency_notification_table(models.Model):
    notification=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    FLAT_OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)


class book_common_area(models.Model):
    FLAT_OCCUPANT=models.ForeignKey(flat_occupant,on_delete=models.CASCADE)
    area=models.CharField(max_length=100)
    date=models.DateField()


class suspicious_activities(models.Model):
    CAMERA=models.ForeignKey(surveillance_camera,on_delete=models.CASCADE)
    image=models.FileField()
    date=models.DateField()
    status=models.CharField(max_length=100,default='notification')



class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
