__all__ = (
    'post_list',
)

from django.shortcuts import render

from ..models import Post

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }

    return render(request, 'posts/post_list.html', context)