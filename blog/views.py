from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import *

from django.urls import reverse

from django.views.generic import View
from .utils import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q


def posts_list(request):

    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_next():
        next_page = page.next_page_number()
    else:
        next_page = ''

    if page.has_previous():
        prev_page = page.previous_page_number()
    else:
        prev_page = ''

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_page': next_page,
        'prev_page': prev_page
    }
    return render(request, 'blog/index.html', context=context)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    template = 'blog/post_update.html'
    form = PostForm
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    template = 'blog/tag_update.html'
    form = TagForm
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'

