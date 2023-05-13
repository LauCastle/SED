from django.urls import path
from tarr import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('singup/', views.singup, name='singup'),
    path('info/', views.info, name='info'),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name='signin'),
    path('cam/', views.cam, name='cam'),
    path('activate/<uidb64>/<token>', views.activate, name="activate")
]
