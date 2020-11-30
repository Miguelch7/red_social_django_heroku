from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from red_social.models import Post, Profile, Relationship, Comment, Like
from red_social.forms import UserRegister, PostForm, CommentForm, UserChangePassword, UserChangeProfile, UserChangeImage
from django.contrib import messages
# Para cambiar contraseña
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash

# Create your views here.
def feed(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'social/feed.html', context)
    else:
        return redirect('login')

@login_required
def feed_following(request, username):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'social/feed_following.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Primera forma
            # username = form.cleaned_data['username']
            # user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            if form.cleaned_data['image']:
                profile.image = form.cleaned_data['image']
            profile.save()
            if profile is not None:
                login(request, user)
                messages.success(request, f'Usuario {user.username} ha sido creado correctamente')
                return redirect('feed')
    else:
        print('User')
        form = UserRegister()

    context = {'form': form}
    return render(request, 'social/register.html', context)


def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    context = {'user': user, 'posts': posts}
    return render(request, 'social/profile.html', context)

@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserChangeProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{user.username}: Los cambios se han realizado éxitosamente')
            return redirect('profile', user.username)
    else:
        form = UserChangeProfile(instance=user)
    context = {'form': form}
    return render(request, 'social/profile_edit.html', context)

@login_required
def change_image(request, username):
    profile = get_object_or_404(Profile, user=request.user )
    image_profile = profile.image.url
    if request.method == 'POST':
        form = UserChangeImage(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto de perfil actualizada')
            return redirect('profile', request.user)
    form = UserChangeImage(instance=profile)
    context = {'form': form, 'image_profile': image_profile}
    return render(request, 'social/change_image.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserChangePassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Importante para actualizar la sesión del user!
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('feed')
        else:
            messages.error(request, 'Ocurrió un error. Inténtalo neuvamente.')
    else:
        form = UserChangePassword(request.user)
    context = {'form': form}
    return render(request, 'social/change_password.html', context)


@login_required
def profile_delete(request, username):
    profile = get_object_or_404(User, username=username)
    if profile:
        profile.delete()
        messages.error(request, 'Usuario eliminado')
    return redirect('feed')

@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post enviado')
            return redirect('feed')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'social/post.html', context)


def post_view(request, id):
    # Obteniendo post
    post = Post.objects.get(pk=id)
    # Obteniendo comentarios
    comments = Comment.objects.filter(to_post=id)
    # Obteniendo usuario en sesion
    current_user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.from_user = current_user
            comment.to_post = post
            comment.save()
            messages.success(request, 'Comentario añadiddo')
            return redirect('post', id)
    else:
        form = CommentForm()
        liked = False
        disliked = False
        if Like.objects.filter(to_post=post.id, from_user=current_user.id, type='L').exists():
            liked = True
        if Like.objects.filter(to_post=post.id, from_user=current_user.id, type='D').exists():
            disliked = True

    context = {'post': post, 'comments': comments, 'form': form, 'liked': liked, 'disliked': disliked}
    return render(request, 'social/post_view.html', context)

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post actualizado!')
            return redirect('post', id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'social/post_edit.html', context)


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, pk=id)
    if post:
        post.delete()
        messages.error(request, f'Post eliminado.')
    return redirect('feed')


@login_required
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Ahora sigues a {username}')
    return redirect('profile', to_user_id)


@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.error(request, f'Dejaste de seguir a {username}')
    return redirect('profile', to_user_id)


@login_required
def like(request, id):
    current_user = request.user
    post = get_object_or_404(Post, pk=id)
    if Like.objects.filter(to_post=post.id, from_user=current_user.id, type='L').exists():
        like = Like.objects.filter(to_post=post.id, from_user=current_user.id)
        like.delete()
        messages.error(request, 'Like removido')
    elif Like.objects.filter(to_post=post.id, from_user=current_user.id, type='D').exists():
        like = Like.objects.filter(to_post=post.id, from_user=current_user.id)
        like.delete()
        like = Like(from_user=current_user, to_post=post, type='L')
        like.save()
        messages.success(request, 'Like!')
    else:
        like = Like(from_user=current_user, to_post=post, type='L')
        like.save()
        messages.success(request, 'Like!')
    return redirect('post', post.id)


@login_required
def dislike(request, id):
    current_user = request.user
    post = get_object_or_404(Post, pk=id)
    if Like.objects.filter(to_post=post.id, from_user=current_user.id, type='D').exists():
        like = Like.objects.filter(to_post=post.id, from_user=current_user.id)
        like.delete()
        messages.error(request, 'Dislike removido')
    elif Like.objects.filter(to_post=post.id, from_user=current_user.id, type='L').exists():
        like = Like.objects.filter(to_post=post.id, from_user=current_user.id)
        like.delete()
        like = Like(from_user=current_user, to_post=post, type='D')
        like.save()
        messages.success(request, 'Dislike!')
    else:
        like = Like(from_user=current_user, to_post=post, type='D')
        like.save()
        messages.success(request, 'Dislike!')
    return redirect('post', post.id)


@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, pk=id)
    post_id = comment.to_post.id
    if comment:
        comment.delete()
        messages.error(request, 'Comentario eliminado')
    return redirect('post', post_id)
