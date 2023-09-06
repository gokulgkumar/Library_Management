from datetime import datetime,timedelta
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from lib_app.models import UserModal,BookModal,RentModal,FineModal,ReturnedModal,CartModal,OrderModal,RentHistoryModaltesting,OrdersModal
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.utils import timezone
import re
# Create your views here.



#Library Home Page
def libraryhomePage(request):
    return render(request,'LibraryHome.html')

#Library About Page
def libraryhomeAboutPage(request):
    return render(request,'LibraryHomeAbout.html')


#Library Contact Page
def libraryhomeContactPage(request):
    return render(request,'LibraryHomeContact.html')

#library home Books
def libraryhomeBooks(request):
    book=BookModal.objects.all
    return render(request,'LibraryHomeBooks.html',{'books':book})


#home page book search results
def LibraryHomeSearchResults(request):
    if request.method=='GET':
        usersearch=request.GET.get('search')
        if usersearch:
            book=BookModal.objects.filter(Q(Book_name__icontains=usersearch) | Q(Author_name__icontains=usersearch))
            return render(request,'LibraryHomeSearchResults.html',{'books':book})
        else:
            raise Http404("Sorry we can't find any matching records")
    else:
        messages.error(request,"Invalid request")
        return render(request,'LibraryHomeSearchResults.html')
            


#Admin Home Page
def adminPage(request):
    message=RentHistoryModaltesting.objects.filter(Due_date__lt=timezone.now().date(),is_returned=False)
    print(message,'message is')
    usercount=User.objects.filter(is_active=0).count()
    # alerts=[]
    overdue_alerts = {}
    for items in message:
        user=items.user
        book = items.User_Rent_Book
        if user not in overdue_alerts:
         overdue_alerts[user] = set()

        alert_msg = (
            f"The user has not returned the book '{book.Book_name}'. "
            f"The due date was {items.Due_date}."
        )
        overdue_alerts[user].add(alert_msg)


    # for items in message:
    #     if items.Due_date < timezone.now().date() and not items.is_returned:
    #         alert_msg=f" The user '{ items.user.first_name}' has not returned the book '{items.User_Rent_Book.Book_name}'. The due date was {items.Due_date} "
    #         alerts.append(alert_msg)
    return render(request,'AdminHome.html',{'overdue_alerts':overdue_alerts,'usercount':usercount})

#User Home Page

def userhomePage(request):
    user=request.user
    print(user)
    message=RentHistoryModaltesting.objects.filter(Due_date__lt=timezone.now().date(),is_returned=False,user=user)
    alerts=[]
    for items in message:
      if items.Due_date < timezone.now().date() and not items.is_returned:
             alert_msg=f"The book '{items.User_Rent_Book.Book_name}' is overdue. Please return the book as soon as possible"
             alerts.append(alert_msg)

    # 
    #     user=items.user
    #     book = items.User_Rent_Book
    #     if user not in overdue_alerts:
    #      overdue_alerts[user] = set()

    #     alert_msg = (
    #         f"You have not returned the book '{book.Book_name}'. "
    #         f"The due date was {items.Due_date}."
    #     )
    #     overdue_alerts[user].add(alert_msg)
    return render(request,'UserHome.html',{'user':user,'alerts':alerts})

       

    
    #return render(request,'UserHome.html',{'users':user})


#login Page
def loginPage(request):
    return render(request,'LoginPage.html')




#login form
def loginform(request):
    if request.method=='POST':
        log_username=request.POST['loguname']
        log_password=request.POST['logpass']
        print(log_username)
        print(log_password)
        user=auth.authenticate(username=log_username,password=log_password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('adminPage')
            else:
                login(request,user)
                auth.login(request,user)
                return redirect('userhomePage')
                    
    messages.info(request,'Invalid Login Credentials / Wait for Approval')
    return redirect('loginPage')
                
                



#signup Page
def signupPage(request):
    return render(request,'SignUp.html')


#generate passcode
def generate_passcode():
    return str(random.randint(100000, 999999))


#Registration form
def signupregistform(request):
    if request.method=='POST':
        reg_fname=request.POST['regfname']
        reg_lname=request.POST['reglname']
        reg_uname=request.POST['reguname']
        reg_uemail=request.POST['reguemail']
        reg_phnnumber=request.POST['regphnnum']
        passcode=generate_passcode()
        print(passcode)
        if not reg_fname.isalpha():
            messages.info(request,'First name must contain only alphabetic characters')
            return redirect('signupPage')
        if not reg_lname.isalpha():
            messages.info(request,'Last name must contain only alphabetic characters')
            return redirect('signupPage')
        if User.objects.filter(username=reg_uname).exists():
            messages.info(request,'Username already exists')
            return redirect('signupPage')
        if User.objects.filter(email=reg_uemail).exists():
            messages.info(request,'Email already exists')
            return redirect('signupPage')
        if not reg_phnnumber.isdigit():
            messages.info(request,'Phone number should contain only numbers')
            return redirect('signupPage')
        if len(reg_phnnumber)>10 or len(reg_phnnumber)<10:
            messages.info(request,'Phone number should contain 10 digits')
            return redirect('signupPage')
        user=User.objects.create_user(first_name= reg_fname,last_name=reg_lname,username=reg_uname,password=passcode,email=reg_uemail,is_active=False)
        user.save()
        data=User.objects.get(id=user.id)
        User_data=UserModal(Phone_number=reg_phnnumber,user=data)
        User_data.save()
        send_mail('Passcode for Login',f'Hi {reg_fname},\n   your registration has been succesful. You can login to your account using this passcode.\nYour passcode is: { passcode }\n\n Thank you.',settings.EMAIL_HOST_USER,[reg_uemail])
        messages.info(request,'Registration successful, Check your email for passcode to login')
        return redirect('loginPage')
            
#logout
@login_required(login_url='loginform')
def logout(request):
    auth.logout(request)
    return redirect('loginPage')

#login required
@login_required(login_url='loginform')
def loginrequired(request):
    return render(request,'LoginPage.html')

#approval request
def approval(request):
    user=User.objects.filter(is_active=0)
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'userRequestAdmin.html',{'users':user,'usercount':usercount})


#approving user request
def approvingrequest(request,uid):
    user=User.objects.get(id=uid)
    user.is_active=True
    user.save()
    messages.info(request,f'{user} has been approved' )
    return redirect('approval')

#user Profile
def userProfile(request,uid):
    user=User.objects.get(id=uid)
    data=UserModal.objects.get(user_id=uid)
    return render(request,'UserProfile.html',{'user':user,'datas':data})

#user book 
def userBook(request):
    user=request.user
    book=BookModal.objects.all
    return render(request,'UserBooks.html',{'books':book,'user':user})

#user search page
def usersearchPage(request):
    book=BookModal.objects.all
    return render(request,'UserBooks.html',{'books':book})


#user search results
def usersearchResults(request):
    if request.method=='GET':
        usersearch=request.GET.get('search')
        
        if usersearch:
            book=BookModal.objects.filter(Book_name__icontains=usersearch) or BookModal.objects.filter(Author_name__icontains=usersearch)
            return render(request,'UserSearchResults.html',{'books':book})
        else:
            messages.info(request,"Sorry Can't find any matching records")
            return render(request,'UserSearchResults.html',{'books':book})
    else:
        messages.error(request,"Invalid request")
        return render(request,'LibraryHomeSearchResults.html')

#user Cart Page
def UserCart(request):
    user=request.user.id
    cart=CartModal.objects.filter(user_id=user)
    return render(request,'CartPage.html',{'carts':cart})



#UserCart
def UserCartAdd(request,cid):
    book=BookModal.objects.get(id=cid)
    bookid=book.id
    users=request.user.id
    cart=CartModal(user_id=users,Book_id=bookid)
    
    cart.save()
    return redirect('UserCart')

#user cart delete
def cartdelete(request,cid):
    cart=CartModal.objects.get(id=cid)
    print(cart)
    cart.delete()
    return redirect('UserCart')

#user payment
def Paymentpage(request):
  user=request.user
  print(user,'user is')
  carts = CartModal.objects.filter(user=request.user.id)
  totalprice=0

  if request.method=='POST':
   cartqu={}
   totalprice=0
   for h in carts:
       cartid=h.id 
       cartquan=int(request.POST.get(f'uquantity{cartid}',0)) 
       if cartquan>0:
            cartqu[cartid]=cartquan
            
            bookprice=int(h.Book.Price)
            print(cartqu[cartid],'quant')

            available_stock=int(h.Book.Stock)

            if available_stock >= cartqu[cartid]:
               h.Book.Stock =str(available_stock - cartqu[cartid])
               h.Book.save()
               cart=OrderModal(Quantity=cartqu[cartid],user=user,Book=h.Book)
               cart.save()
               price= int(bookprice * cartqu[cartid])
               print(price,'price is')
               totalprice += price
               print(totalprice,'total price in loop')
            else:
             print(f'insufficient stock for {h.Book.Book_name}')
       
        
  print(totalprice,'price is')
  
  order=OrderModal.objects.filter(user=user)

  
#   order.totalprice=totalprice
 
    #    order=OrderModal(user=user,Book=carts.Book,Quantity=cartqu[cartid])
  return render(request,'OrderPayment.html',{'totalprice':totalprice,'user':user})
       
  



def confirm(request,uid):
     user=request.user
     email=user.email
     print(user,'user')
     order=OrderModal.objects.filter(user_id=uid)
     cart=CartModal.objects.filter(user_id=uid)
     Order_date = datetime.now()
     booknames=[]
     totalprice=0
     
     for b in order:
        booknames.append(b.Book.Book_name)
        totalprice += int(b.Book.Price) * int(b.Quantity) 
        
        print(b.Price,'price')
    
     send_mail('Order Details',f'Hi { user.first_name },\n\n  Your order for the books {", ".join(booknames)} has been successful. \n\nTotal Price: ₹{totalprice}\n\nThank you for your purchase!!',settings.EMAIL_HOST_USER,[email])
     orders=OrdersModal(user=user,Order_date=Order_date,Price=totalprice,BooksName=booknames)
     orders.save()
     cart.delete()
     order.delete()
     
     print(booknames, 'the booknames are')
     return render(request,'Userorderconfirmed.html')




#User Rent Book Page
def UserRentBookPage(request,uid):
    rentaldiscountcharge=50
    book=BookModal.objects.get(id=uid)
    print(book,'book no:')
    bookprice=int(book.Price) - rentaldiscountcharge
    return render(request,'UserRentBook.html',{'books':book,'bookprices':bookprice})

#User rent
def rent(request,bid):
    if request.method=='POST':
        book=BookModal.objects.get(id=bid)
        user=request.user
        name=user.first_name
        email=user.email
        bookstock=int(book.Stock)
        user_period_days=int(request.POST.get('rentdays'))
        user_quantity=int(request.POST.get('rentquantity'))

        if user_quantity > bookstock:
            return HttpResponse("Insufficient stock, please return back and enter correct value")

        if user_quantity>0:
            bookstock=int(book.Stock)
            bookstock -= user_quantity
            book.Stock=bookstock
            book.save()

        if user_quantity<=0 or user_quantity == '':
            return HttpResponse("Invalid quantity value, please return back and enter correct value")

        if user_period_days<0 or user_quantity == '':
            return HttpResponse("Invalid period value, please return back and enter correct value")
        
        current_date=datetime.now()
        due_date=current_date + timedelta(days=user_period_days)

        date_formail=due_date.strftime('%Y-%m-%d')
        

        user_rent=RentModal(Due_date=due_date, Rent_date= current_date, User_Rent_Book=book, user=user, Rental_period=user_period_days, Rental_books_quantity=user_quantity)
        renthistory = RentHistoryModaltesting(Due_date=due_date, Rent_date= current_date, User_Rent_Book=book, user=user, Rental_period=user_period_days, Rental_books_quantity=user_quantity)
        user_rent.save()
        renthistory.save()

        send_mail('Book Rental',f'Hi { name },\n\n Your submission for book rental has been successful.\n\n You should return your book by {date_formail}. If not additional charges may apply.\n\n Thank you.',settings.EMAIL_HOST_USER,[email])
        return redirect('UserRentalSuccess')
    
    return HttpResponse("You missed a field please go back and enter the correct value")



#User rental success Page
def UserRentalSuccess(request):
    user=request.user
    return render(request,'UserRentalSuccess.html',{'user':user})

#User Rent Return Page
def UserRentReturn(request,uid):
    rentedbook=RentModal.objects.filter(user_id=uid)
    return render(request,'UserRentReturn.html',{'rentedbooks':rentedbook})


def UserBookLostPage(request):
    user=request.user.id
    fine=FineModal.objects.get(user_id=user)
    return render(request,'UserBookLostPage.html',{'fine':fine})
  

    # totalfine=0
    # for f in getobj:
    #     bookPrice=int(f.User_Rent_Book.Price)
    #     bookQuantity=int(f.Rental_books_quantity)
    #     bookStock=int(f.User_Rent_Book.Stock)
    #     addcharge=500
    #     fine= addcharge +  bookPrice * bookQuantity

    #     bookStock -= bookQuantity

    #     f.User_Rent_Book.save()

    #     totalfine+=fine
    

    # print(totalfine,'fine')
    # print(user,'user')


    return HttpResponse("good")

#User Book Lost
def UserBookLost(request,bid):
    user=request.user.id
    book=RentModal.objects.get(id=bid)
    bookid = book.User_Rent_Book_id

    quantity=int(book.Rental_books_quantity)
    print(quantity,'quantity')
    print(bookid,'bookid')

    bookorgid=BookModal.objects.get(id=bookid)
    OriginalPrice=int(bookorgid.Price)
    Fineamount=500
    Fine=Fineamount + (OriginalPrice * quantity)
    # bookstock=int(bookorgid.Stock)
    # if bookstock == 0:
    #     stock=0
    #     bookorgid.Stock=stock
    #     bookorgid.save()

    # else:
    #     bookstock -= quantity
    #     bookorgid.Stock=bookstock
    #     bookorgid.save()
    return render(request,'UserBookLostPage.html',{'fine':Fine,'book':book})
    

    # print(Fine)
    # print(user)

    
    #messages.warning(request,f'Since the book was lost a fine of ₹{fine} has to be paid')
    


def UserBookLostPay(request,fid):
    rent=RentModal.objects.get(id=fid)
    print(rent.id,'id is')
    # user=request.user.id
    histid=int(fid) - 1
    history=RentHistoryModaltesting.objects.get(id=histid)
    print(history.id,'history id is')
    
   
    history.is_lost = True
    history.is_returned = True
    history.save()
    rent.delete()
    
    return render(request,'UserBookLostPayment.html')



def lostpaymentsuccess(request):
    return render(request,'UserBookLostPaymentSuccessOne.html')

#book lost payment card
def lostcard(request):
    return render(request,'UserBookLostPaymentSuccessOne.html')

#user rental history
def rentalHistory(request,rid):
    print(rid,'request id')
    history=RentHistoryModaltesting.objects.filter(user_id=rid)
    return render(request,'UserRentalHistory.html',{'histories':history})

#User late
def UserReturnLate(request,bid):
    returns=ReturnedModal.objects.get(id=bid)
    returns.is_returned=True
    return request(request,'UserReturnLate.html')




#return book user
def returnbook(request,bid):
    rent=RentModal.objects.get(id=bid)
    
    
    user =request.user
    quantity =int(rent.Rental_books_quantity)
    print(quantity,'rental quantity')


    bookid = rent.User_Rent_Book_id
    
    

    book=BookModal.objects.get(id=bookid)

    history=RentHistoryModaltesting.objects.filter(user_id=user,User_Rent_Book_id=bookid)
    
    
    bookstock=int(book.Stock)
    print(bookstock)


    rentdate = rent.Rent_date
    duedate=rent.Due_date

    print(duedate,'due date')
    print(rentdate,'rent date')

    return_date=datetime.now().date()
    print(return_date,'current date')

    if return_date > duedate:
        
        late = return_date - duedate
        dayslate=late.days

        fine=10
        finalfine=dayslate*fine
        print(finalfine)
        fines=ReturnedModal(Fine=finalfine,Return_date=return_date,Rent_details=rent,user=user)
        bookstocks = bookstock + quantity
        book.Stock = bookstocks

        for entry in history:
            entry.Returned_date = return_date
            entry.is_returned = True
            entry.save()

        book.save()
        fines.save()
         
        print(fines)
        return render(request,'UserReturnLate2.html',{'user':user,'fines':fines})
    
    else:
        bookstocks = bookstock + quantity
        book.Stock = bookstocks
        book.save()

        #rent.Returned_date=return_date
        returned=ReturnedModal(Return_date=return_date,Rent_details=rent,user=user,Fine=0,is_returned=True)
        
        for entry in history:
            entry.Returned_date = return_date
            entry.is_returned = True
            entry.save()
        
        returned.save()
        rent.delete()
        return render(request,'UserReturnLate.html',{'user':user})
    

def userreturnlatefine(request,uid):
    users=request.user.id
    returnfine=ReturnedModal.objects.filter(id=uid)
    return render(request,'UserreturnPayment.html',{'returnfines':returnfine,'users':users})


def returncard(request,uid):
     return_date=datetime.now().date()
     rent=RentModal.objects.filter(user_id=uid)
     history=RentHistoryModaltesting.objects.filter(user_id=uid)
     for entry in history:
         entry.is_returned=True
         entry.Returned_date = return_date
         entry.save()
    
     returned = ReturnedModal.objects.filter(id=uid)
     for entries in returned:
         entries.is_returned=True
         entries.save()

     rent.delete()
     return render(request,'UserFineSuccess.html')





##################
def editUserPage(request,uid):
    user=User.objects.get(id=uid)
    data=UserModal.objects.get(user_id=uid)
    return render(request,'UserEditPage.html',{'users':user,'datas':data})






def editUserDetails(request,uid):
    if request.method=='POST':
        user=User.objects.get(id=uid)
        data=UserModal.objects.get(user_id=uid)
        user.first_name=request.POST['upfname']
        user.last_name=request.POST['uplname']
        user.username=request.POST['upuname']
        user.email=request.POST['upuemail']
        data.Phone_number=request.POST['upphnnum']
        user.save()
        data.save()
    messages.info(request,'Details Updated')
    return redirect('editUserPage',uid=uid)


def UserPasswordConfirm(request,uid):
    if request.method=='POST':
        user=User.objects.get(id=uid)
        newpass=request.POST['upass']
        cnewpass=request.POST['cupass']
        if( newpass=='' and cnewpass==''):
            messages.info(request,'Password field cannot be empty')
            return redirect('editUserPassword')
        elif(newpass==cnewpass):
            if (
                len(newpass) >= 8 and any(char.isdigit() for char in newpass) and
                any(char.isupper() for char in newpass) and re.search(r'[!@#$%^&*(),.?\":{}|<>]', newpass)
            ):
                user.set_password(newpass)
                user.save()
                messages.info(request, 'Password Changed, Login to continue')
                return redirect('loginPage')
            else:
                messages.info(request, 'Password should contain at least 8 characters, at least one digit, one uppercase letter, and one special character')
                return redirect('editUserPassword',uid=uid)
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('editUserPassword',uid=uid)




def editUserPassword(request,uid):
    user=User.objects.get(id=uid)
    return render(request,'UserPassword.html',{'users':user})



#user edit details
#def editUserDetails(request, uid):
    if request.method == 'POST':
        user = User.objects.get(id=uid)
        usermod = UserModal.objects.get(user_id=uid)

        user_pass = request.POST['uppasswrd']
        user_conpass = request.POST['conuppasswrd']

        user.first_name = request.POST['upfname']
        if not user.first_name.isalpha():
            messages.info(request, 'First name must contain only alphabetic characters')
            return render(request, 'UserEditError.html')

        user.last_name = request.POST['uplname']
        if not user.last_name.isalpha():
            messages.info(request, 'Last name must contain only alphabetic characters')
            return render(request, 'UserEditError.html')

        user.username = request.POST['upuname']
        user.email = request.POST['upuemail']

        usermod.Phone_number = request.POST['upphnnum']
        if not usermod.Phone_number.isdigit():
            messages.info(request, 'Phone number should contain only numbers')
            return render(request, 'UserEditError.html')
        if len(usermod.Phone_number) != 10:  # Changed the condition to exactly 10 digits
            messages.info(request, 'Phone number should contain 10 digits')
            return render(request, 'UserEditError.html')

        user.save()
        usermod.save()

        if user_pass == '' and user_conpass == '':
            messages.info(request, 'Password field cannot be blank!!')
            return render(request, 'UserEditError.html')

        elif user_pass == user_conpass:
            if (
                len(user_pass) >= 8 and any(char.isdigit() for char in user_pass) and
                any(char.isupper() for char in user_pass) and re.search(r'[!@#$%^&*(),.?\":{}|<>]', user_pass)
            ):
                user.set_password(user_pass)
                user.save()
                messages.info(request, 'Details have been Updated')
                return render(request,'UserProfile.html')

            else:
                messages.info(request, 'Password should contain at least 8 characters, at least one digit, one uppercase letter, and one special character')
                return render(request, 'UserEditError.html')

        else:
            messages.info(request, 'Password does not match')
            return render(request, 'UserEditError.html')

    



    

        

            
#orders
def AdminUserOrders(request):
    orders=OrdersModal.objects.all()
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminUserOrders.html',{'orders':orders,'usercount':usercount})






# Admin Book
def BookAdmin(request):
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminBook.html',{'usercount':usercount})

#Admin Add Book Page
def adminAddBookPage(request):
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminAddBook.html',{'usercount':usercount})

#admin Add Book
def adminAddBook(request):
    if request.method=='POST':
        bk_name=request.POST['bname']
        bk_author=request.POST['bauthor']
        bk_publisher=request.POST['bpublisherid']
        bk_stock=request.POST['bstock']
        bk_price=request.POST['bprice']
        bk_image=request.FILES.get('bimage')
        book=BookModal(Book_name=bk_name,Author_name=bk_author,Publisher_ID=bk_publisher,Stock=bk_stock,Price=bk_price,Book_Image=bk_image)
        book.save()
        messages.success(request,'Book has been added successfully')
        return redirect('adminAddBookPage')
        

#admin view book Page
def adminViewBook(request):
    book=BookModal.objects.all
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminViewBook.html',{'books':book,'usercount':usercount})

#admin edit book Page
def adminEditBookPage(request,bid):
    book=BookModal.objects.get(id=bid)
    return render(request,'AdminEditBook.html',{'books':book})

#admin Edit Book
def adminEditBook(request,bid):
    if request.method=='POST':
        book=BookModal.objects.get(id=bid)
        book.Book_name=request.POST['bname']
        book.Author_name=request.POST['bauthor']
        book.Publisher_ID=request.POST['bpublisherid']
        book.Stock=request.POST['bstock']
        book.Price=request.POST['bprice']
        Book_oldImage=book.Book_Image
        Book_newImage=request.FILES.get('bimage')
        if Book_oldImage!= None and Book_newImage==None:
            book.Book_Image=Book_oldImage
        else:
            book.Book_Image=Book_newImage
        book.save()
        return redirect('adminViewBook')
    return render(request,'AdminEditBook.html')


#admin delete Book
def adminDeleteBook(request,bid):
    book=BookModal.objects.get(id=bid)
    book.delete()
    return redirect('adminViewBook')


#admin user 
def AdminUser(request):
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminUser.html',{'usercount':usercount})

#admin user registered
def AdminUserReg(request):
    user=UserModal.objects.all()
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminRegisteredUsers.html',{'user':user,'usercount':usercount})

#admin user rents
def AdminUserRents(request):
    rent=RentHistoryModaltesting.objects.all()
    usercount=User.objects.filter(is_active=0).count()
    return render(request,'AdminUserRents.html',{'rent':rent,'usercount':usercount})
