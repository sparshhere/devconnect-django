from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .forms import (
    PostForm,
    CommentForm,
    EmailPostForm,
    SearchForm,
)
from django.db.models import Count
from django.core.paginator import Paginator

def post_list(request):

    post_list = Post.published.all()

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(
        request,
        'posts/post/list.html',
        {
            'posts': posts
        }
    )


def post_detail(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        status='published'
    )

    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list(
    'id',flat=True)

    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)

    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    new_comment = None

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)

            new_comment.post = post

            new_comment.save()

    else:

        comment_form = CommentForm()

    return render(
        request,
        'posts/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
        }
    )

def post_share(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        status='published'
    )

    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            subject = (
                f"{cd['name']} recommends "
                f"you read {post.title}"
            )

            message = (
                f"Read {post.title} at "
                f"{post_url}\n\n"
                f"{cd['name']} comments: "
                f"{cd['comments']}"
            )

            send_mail(
                subject,
                message,
                None,
                [cd['to']]
            )

            sent = True

    else:

        form = EmailPostForm()

    return render(
        request,
        'posts/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@login_required
def post_create(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.user = request.user

            post.save()

            form.save_m2m()

            return redirect(post.get_absolute_url())

    else:

        form = PostForm()

    return render(
        request,
        'posts/post/create.html',
        {'form': form}
    )


@login_required
def post_update(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = PostForm(
            instance=post,
            data=request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(post.get_absolute_url())

    else:

        form = PostForm(instance=post)

    return render(
        request,
        'posts/post/create.html',
        {
            'form': form,
            'post': post
        }
    )


@login_required
def post_delete(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        user=request.user
    )

    post.delete()

    return redirect('post_list')

def post_search(request):

    form = SearchForm()

    query = None

    results = []

    if 'query' in request.GET:

        form = SearchForm(request.GET)

        if form.is_valid():

            query = form.cleaned_data['query']

            results = Post.published.filter(
                title__icontains=query
            )

    return render(
        request,
        'posts/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results,
        }
    )
@login_required
def post_like(request, id):

    post = get_object_or_404(
        Post,
        id=id
    )

    if request.user in post.users_like.all():

        post.users_like.remove(request.user)

    else:

        post.users_like.add(request.user)

    return redirect(post.get_absolute_url())