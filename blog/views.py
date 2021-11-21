from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .models import Post
from django.contrib import messages


def view_blog(request):
    blog_posts = Post.objects.all()

    return render(request, "blog/blog.html", {"blog_posts": blog_posts, })


@login_required
def create_post(request):
    """Add a post to the blog"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admins can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save()
            messages.success(request, "Post added successfully!")
            blog_posts = Post.objects.all()

            return render(request, "blog/blog.html", {"blog_posts": blog_posts, })
        else:
            messages.error(
                request, "Failed to add post. \
                    Please ensure the form is valid."
            )
    else:
        form = BlogForm()

    template = "blog/create_post.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """Delete a product from the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admins can do that.")
        return redirect(reverse("home"))

    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, "Post deleted!")

    blog_posts = Post.objects.all()

    return redirect(reverse("view_blog"))