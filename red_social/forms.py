from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from red_social.models import Post, Comment, Profile

class UserRegister(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
    image = forms.ImageField(label='Foto de Perfil', widget=forms.FileInput(attrs={'name': 'profile_image', 'id': 'profile_image'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']
        help_texts = {k:'' for k in fields}


class UserChangeProfile(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {k:'' for k in fields}


class UserChangeImage(forms.ModelForm):
    image = forms.ImageField(label='Foto de Perfil', widget=forms.FileInput(attrs={'name': 'profile_image', 'id': 'profile_image'}), required=False)

    class Meta:
        model = Profile
        fields = ['image']


class UserChangePassword(PasswordChangeForm):

    class Meta:
        model = User
        fields = '__all__'
        help_texts = {k:'' for k in fields}


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué estás pensando?'}), required=True)

    class Meta:
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Comentario', widget=forms.Textarea(attrs={'rows':1, 'placeholder': 'Añade un comentario...'}))

    class Meta:
        model = Comment
        fields = ['content']
