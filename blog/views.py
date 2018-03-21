from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.http import HttpResponseNotFound, Http404

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.visits += 1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if not request.user.is_authenticated():
        return redirect('post_list')
        # raise Http404()
        #return HttpResponseNotFound('<h1>404 - Not found :(</h1>')


    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})