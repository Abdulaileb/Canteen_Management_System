# from django.db import models
# from  django.utils import timezone

# # Create your models here.


# class Transaction(models.Model):
#     Company_Name = models.CharField(max_length=50, blank=False,)
#     Name = models.CharField(max_length=100)
#     Business = models.CharField(max_length=40, choices=VENDOR_CHOICES, default='Manufacturer')
#     Address = models.CharField(max_length=250)
#     City = models.CharField(max_length=30, null=True, blank=True)
#     Phone = models.CharField(max_length=15)
#     Email = models.EmailField(max_length=50, null=True, blank=True)
#     Website = models.URLField(max_length=250, blank=True, null=True)
#     Country = CountryField(blank_label='(select country)')

#     def __str__(self):
#         return self.Company_Name
    
# class Order(models.Model):
#     Company_Name = models.CharField(max_length=50, blank=False,)
#     Name = models.CharField(max_length=100)
#     Business = models.CharField(max_length=40, choices=VENDOR_CHOICES, default='Manufacturer')
#     Address = models.CharField(max_length=250)
#     City = models.CharField(max_length=30, null=True, blank=True)
#     Phone = models.CharField(max_length=15)
#     Email = models.EmailField(max_length=50, null=True, blank=True)
#     Website = models.URLField(max_length=250, blank=True, null=True)
#     Country = CountryField(blank_label='(select country)')

#     def __str__(self):
#         return self.Company_Name
    
# class Transaction(models.Model):
#     Company_Name = models.CharField(max_length=50, blank=False,)
#     Name = models.CharField(max_length=100)
#     Business = models.CharField(max_length=40, choices=VENDOR_CHOICES, default='Manufacturer')
#     Address = models.CharField(max_length=250)
#     City = models.CharField(max_length=30, null=True, blank=True)
#     Phone = models.CharField(max_length=15)
#     Email = models.EmailField(max_length=50, null=True, blank=True)
#     Website = models.URLField(max_length=250, blank=True, null=True)
#     Country = CountryField(blank_label='(select country)')

#     def __str__(self):
#         return self.Company_Name