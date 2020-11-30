from django.urls import path
# Importando vistas individualmente
#from .views import feed, profile, register, post, follow, unfollow
# Importando todas las vistas
from .views import *
# Importamos estos 2 modulos para poder ver las imagenes subidas usuario
# en modo de desaroollo
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', feed, name='feed'),
    path('feed/<str:username>/', feed_following, name='feed_following'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/edit/<str:username>/', profile_edit, name='profile_edit'),
    path('profile/edit/image/<str:username>/', change_image, name='change_image'),
    path('change_password/', change_password, name='change_password'),
    path('profile/delete/<str:username>/', profile_delete, name='profile_delete'),
    path('follow/<str:username>/', follow, name='follow'),
    path('unfollow/<str:username>/', unfollow, name='unfollow'),
    path('post/', post, name='post'),
    path('post/<int:id>/', post_view, name='post'),
    path('post/<int:id>/edit/', post_edit, name='post_edit'),
    path('post/<int:id>/delete/', post_delete, name='post_delete'),
    path('post/<int:id>/like/', like, name='post_like'),
    path('post/<int:id>/dislike/', dislike, name='post_dislike'),
    path('comment/delete/<int:id>', comment_delete, name='comment_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
