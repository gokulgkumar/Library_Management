from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone

# Create your models here.



#Book
class BookModal(models.Model):
    Book_name= models.CharField(max_length=250)
    Author_name=models.CharField(max_length=250)
    Price = models.CharField(max_length=250)
    Publisher_ID=models.CharField(max_length=25)
    Stock=models.CharField(max_length=250)
    Book_Image=models.ImageField(upload_to="image/",null=True)
    Book_date=models.DateField(auto_now_add=True)
    


#User
class UserModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Phone_number=models.CharField(max_length=10)
    User_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    User_date=models.DateField(auto_now_add=True)
    
############################


#renthistory test
class RentHistoryModaltesting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    User_Rent_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Rent_date=models.DateField(default=timezone.now)
    Due_date=models.DateField()
    Rental_period=models.CharField(max_length=50)
    Rental_books_quantity=models.CharField(max_length=50)
    Returned_date=models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)



#######################
#RentalModal
class RentModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    User_Rent_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Rent_date=models.DateField(default=timezone.now)
    Due_date=models.DateField()
    Rental_period=models.CharField(max_length=50)
    Rental_books_quantity=models.CharField(max_length=50)
    Returned_date=models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)

#fine
class FineModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Rent_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Rent_details=models.ForeignKey(RentModal,on_delete=models.CASCADE,null=True)
    Fine=models.CharField(max_length=250)
    is_paid=models.BooleanField(default=False)

class ReturnedModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Rent_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Rent_details=models.ForeignKey(RentModal,on_delete=models.CASCADE,null=True)
    Fine=models.CharField(max_length=250)
    Return_date=models.DateField(null=True, blank=True)
    is_returned=models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)


#ReturnFine
# class ReturnModal(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
#     Rent_Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
#     Rent_details=models.ForeignKey(RentModal,on_delete=models.CASCADE,null=True)
#     Fine=models.CharField(max_length=250)
#     Return_date=models.DateField(null=True, blank=True)



#rent History

#########################


#cart modal
class CartModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Quantity=models.CharField(max_length=50)
    Price=models.CharField(max_length=50)


#OrderModal
class OrderModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    cart=models.ForeignKey(CartModal,on_delete=models.CASCADE,null=True)
    Quantity=models.CharField(max_length=50)
    Price=models.CharField(max_length=50)
    totalprice=models.CharField(max_length=255)

 #totalpriceModal
class TotalPriceModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(OrderModal,on_delete=models.CASCADE,null=True)
    Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    totalprice=models.CharField(max_length=250)



class OrdersModal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(OrderModal,on_delete=models.CASCADE,null=True)
    Book=models.ForeignKey(BookModal,on_delete=models.CASCADE,null=True)
    Price=models.CharField(max_length=250)
    Order_date=models.DateField(null=True, blank=True)
    BooksName=models.CharField(max_length=600)
    
    
