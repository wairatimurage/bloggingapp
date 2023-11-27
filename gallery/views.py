# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

import gallery.views
from .app_form import PostForm, LoginForm
from .models import Post, Category
from django.shortcuts import redirect


@login_required
@permission_required('gallery.view_post', raise_exception=True)
def post_list(request, category=None):
    if category:
        # Use get_object_or_404 to handle the case where the category doesn't exist
        selected_category = get_object_or_404(Category, name=category)
        posts = Post.objects.filter(category=selected_category)
    else:
        posts = Post.objects.all()
        selected_category = None  # No specific category selected

    categories = Category.objects.all()  # Fetch all categories
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'posts': data, 'categories': categories, 'selected_category': selected_category})


@login_required
@permission_required('gallery.view_post', raise_exception=True)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


@login_required
@permission_required('gallery.add_post', raise_exception=True)
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        categories = Category.objects.all()
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form, 'categories': categories})


@login_required
@permission_required('gallery.change_post', raise_exception=True)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        categories = Category.objects.all()
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'categories': categories})


@login_required
@permission_required('gallery.delete_post', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # If the form is submitted, delete the post and redirect to 'post_list'
        post.delete()
        return redirect('post_list')

    # If it's a GET request, render the confirmation page
    return render(request, 'post_delete.html', {'post': post})


def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('post_list')
        messages.error(request, "Wrong username or password")
        return render(request, "login.html", {"form": form})


@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required()
@permission_required('gallery.view_post', raise_exception=True)
def search(request):
    search_word = request.GET["search_word"]
    posts = Post.objects.filter(
        Q(title__icontains=search_word) | Q(content__icontains=search_word)
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    # Elastic search
    return render(request, "post_list.html", {"posts": data})

# @login_required
# @permission_required('gallery.view_post', raise_exception=True)
# def category_posts(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#     posts = Post.objects.filter(category=category)
#     return render(request, 'category_posts.html', {'category': category, 'posts': posts})
