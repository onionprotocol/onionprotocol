from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class AppUser(models.Model):
    #qr_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(default="candidate",max_length=10)

    otp_code = models.CharField(default="none",max_length=10)

    passphrase0 = models.CharField(default="none",max_length=20)
    passphrase1 = models.CharField(default="none",max_length=20)
    passphrase2 = models.CharField(default="none",max_length=20)
    passphrase3 = models.CharField(default="none",max_length=20)
    passphrase4 = models.CharField(default="none",max_length=20)
    passphrase5 = models.CharField(default="none",max_length=20)
    passphrase6 = models.CharField(default="none",max_length=20)
    passphrase7 = models.CharField(default="none",max_length=20)
    passphrase8 = models.CharField(default="none",max_length=20)
    passphrase9 = models.CharField(default="none",max_length=20)
    passphrase10 = models.CharField(default="none",max_length=20)
    passphrase11 = models.CharField(default="none",max_length=20)
    
    ec_status = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    
    #wallet shit
    wallet_address = models.CharField(default="null",max_length=100)
    wallet_key = models.CharField(default="null",max_length=100)
    
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username