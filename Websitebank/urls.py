import profile
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.homepage, name = "bank-home"),
    path('login/',auth_views.LoginView.as_view(template_name = "login.html"), name = "bank-login"),
    #path('login/',auth_views.LoginView.as_view(template_name = "login.html"), name = "bank-login"),
    path('signup/', views.signup,name = "bank-signup" ),
    path('transactions/', views.transaction, name= "bank-transactions"),
    #path('logout/', views.logout, name = 'bank-logout')
    path('logout/', auth_views.LogoutView.as_view(template_name = "logout.html"),name= "bank-logout"),
    path('profile/', views.profiles, name = 'bank-profiles'),
    path('transactions/',views.transaction,name ="bank-transactions"),
    path('history/', views.history,name = "bank-history"),
    path('nodeflux/', views.nodeflux, name="bank-nodeflux")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

urlpatterns+= staticfiles_urlpatterns()
