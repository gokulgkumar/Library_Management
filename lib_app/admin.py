from django.contrib import admin
from lib_app.models import RentModal,BookModal,UserModal,FineModal,RentHistoryModaltesting

# Register your models here.
@admin.register(BookModal)
class BookModalDetailAdmin(admin.ModelAdmin):
    list_display=('id','Book_name','Author_name','Price','Book_date')


@admin.register(UserModal)
class UserModalDetailAdmin(admin.ModelAdmin):
    list_display=('id','user','User_Book','User_date')


@admin.register(RentModal)
class RentModal(admin.ModelAdmin):
    list_display=('id','user','User_Rent_Book','Rent_date','Due_date','Rental_period','Rental_books_quantity','is_returned')


@admin.register(FineModal)
class FineModal(admin.ModelAdmin):
    list_display=('id','user','Rent_Book','Rent_details','Fine','is_paid')


@admin.register(RentHistoryModaltesting)
class RentModal(admin.ModelAdmin):
    list_display=('id','user','User_Rent_Book','Rent_date','Due_date','Rental_period','Rental_books_quantity','is_returned')