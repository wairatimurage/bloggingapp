# views.py

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .form import PostForm
from .models import Post
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


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
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # If the form is submitted, delete the post and redirect to 'post_list'
        post.delete()
        return redirect('post_list')

    # If it's a GET request, render the confirmation page
    return render(request, 'post_delete.html', {'post': post})
