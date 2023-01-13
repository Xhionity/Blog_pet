from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views import View
from django.urls import reverse

from .models import Post, Vote
from .forms import PostForm


def home(request):
    error = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'Form is not correct'

    form = PostForm
    context = {
        'posts': Post.objects.all().order_by('-id'),
        'form': form,
        'error': error,
    }
    return render(request, 'index.html', context)


def edit(request, id):
    try:
        post = Post.objects.get(id=id)

        if request.method == "POST":
            post.title = request.POST.get("title")
            post.content = request.POST.get("content")
            post.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"post": post})
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Пост не найден!</h2>")


def delete(request, id):
    try:
        post = Post.objects.get(id=id)
        post.delete()
        return HttpResponseRedirect('/')
    except Post.DoesNotExist:
        return HttpResponseRedirect('<h2>Пост не найден</h2>')


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Vote.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        return HttpResponseRedirect(reverse('vote', args=[str(pk)]))


class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Vote.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        return HttpResponseRedirect(reverse('vote', args=[str(pk)]))
