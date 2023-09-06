from django.urls import path
from . import views



urlpatterns = [ 

    #library home
    path('',views.libraryhomePage,name='libraryhomePage'),
    path('libraryhomeBooks',views.libraryhomeBooks,name='libraryhomeBooks'),
    path('search',views.LibraryHomeSearchResults,name='search'),
    path('loginrequired',views.loginrequired,name='loginrequired'),
    path('libraryhomeAboutPage',views.libraryhomeAboutPage,name='libraryhomeAboutPage'),
    path('libraryhomeContactPage',views.libraryhomeContactPage,name='libraryhomeContactPage'),

    #admin home page
    path('adminPage',views.adminPage,name='adminPage'),

    #user home page
    path('userhomePage',views.userhomePage,name='userhomePage'),

    #userprofile
    path('userProfile/<int:uid>',views.userProfile,name='userProfile'),

    #user
    path('editUserPage/<int:uid>',views.editUserPage,name='editUserPage'),
    path('userBook',views.userBook,name='userBook'),
    path('search',views.usersearchResults,name='search'),
    path('UserRentBookPage/<int:uid>',views.UserRentBookPage,name='UserRentBookPage'),
    path('rent/<int:bid>',views.rent,name='rent'),
    path('UserRentalSuccess',views.UserRentalSuccess,name='UserRentalSuccess'),
    path('UserRentReturn/<int:uid>',views.UserRentReturn,name='UserRentReturn'),
    path('UserBookLost/<int:bid>',views.UserBookLost,name='UserBookLost'),
    path('UserBookLostPage',views.UserBookLostPage,name='UserBookLostPage'),
    path('UserBookLostPay/<int:fid>',views.UserBookLostPay,name='UserBookLostPay'),
    path('lostcard',views.lostcard,name='lostcard'),
    path('lostpaymentsuccess',views.lostpaymentsuccess,name='lostpaymentsuccess'),
    path('rentalHistory/<int:rid>',views.rentalHistory,name='rentalHistory'),
    path('returnbook/<int:bid>',views.returnbook,name='returnbook'),
    path('UserReturnLate/<int:bid>',views.UserReturnLate,name='UserReturnLate'),
    path('UserCartAdd/<int:cid>',views.UserCartAdd,name='UserCartAdd'),
    path('UserCart',views.UserCart,name='UserCart'),
    path('cartdelete/<int:cid>',views.cartdelete,name='cartdelete'),
    path('Paymentpage',views.Paymentpage,name='Paymentpage'),
    path('confirm/<int:uid>',views.confirm,name='confirm'),
    path('editUserDetails/<int:uid>/',views.editUserDetails,name='editUserDetails'),
    path('editUserPassword/<int:uid>',views.editUserPassword,name='editUserPassword'),
    path('UserPasswordConfirm/<int:uid>',views.UserPasswordConfirm,name='UserPasswordConfirm'),
    path('userreturnlatefine/<int:uid>',views.userreturnlatefine,name='userreturnlatefine'),
    path('returncard/<int:uid>',views.returncard,name='returncard'),
    # path()

    #signup registration
    path('signupPage',views.signupPage,name='signupPage'),
    path('signupregistform',views.signupregistform,name='signupregistform'),

    #loginpage
    path('loginPage',views.loginPage,name='loginPage'),

    #login form
    path('loginform',views.loginform,name='loginform'),


    #approval
    path('approval',views.approval,name='approval'),
    path('approvingrequest/<int:uid>',views.approvingrequest,name='approvingrequest'),

    #admin book
    path('BookAdmin',views.BookAdmin,name='BookAdmin'),
    path('adminAddBookPage',views.adminAddBookPage,name='adminAddBookPage'),
    path('adminAddBook',views.adminAddBook,name='adminAddBook'),
    path('adminViewBook',views.adminViewBook,name='adminViewBook'),
    path('adminEditBookPage/<int:bid>',views.adminEditBookPage,name='adminEditBookPage'),
    path('adminEditBook/<int:bid>',views.adminEditBook,name='adminEditBook'),
    path('adminDeleteBook/<int:bid>',views.adminDeleteBook,name='adminDeleteBook'),
    path('AdminUser',views.AdminUser,name='AdminUser'),
    path('AdminUserReg',views.AdminUserReg,name='AdminUserReg'),
    path('AdminUserRents',views.AdminUserRents,name='AdminUserRents'),
    path('AdminUserOrders',views.AdminUserOrders,name='AdminUserOrders'),

    #logout
    path('logout',views.logout,name='logout')
]