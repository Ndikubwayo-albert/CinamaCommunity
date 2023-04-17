from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePage, LoginPage, Update_Pic, CommentPost, EditPost, DeletePost, Update_Picture, RegisterPage, Update_Profile, Post, Myposts, Profile, verify_email,Dashboard,LogoutPage


urlpatterns = [
    path('', HomePage, name="home"),
    path('login/', LoginPage, name="loginpage"),
    path('logout/', LogoutPage, name="logoutpage"),
    path('create_account/', RegisterPage, name="createaccount"),
    path('verfiy_email/<str:token>', verify_email, name="verify"),
    path('dashboard/', Dashboard, name="dashboard"),
    path('profile/', Profile, name='profile'),
    path('my_posts/', Myposts, name='myposts'),
    path('add_post/', Post, name="post"),
    path('update_profile/', Update_Profile, name="updateprofile"),
    path('update_picture/', Update_Picture, name="updateprofilepic"),
    path('comment/<int:id>/', CommentPost, name="comment"),
    path('delete/<int:id>', DeletePost, name="delete"),
    path('edit/<int:id>', EditPost, name="editpost"),
    path('pic/<int:id>/', Update_Pic, name="updatepostpic")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)