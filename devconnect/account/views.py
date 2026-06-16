from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth.models import User
from .models import Profile

from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)


def register(request):

    if request.method == 'POST':

        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():

            new_user = user_form.save()

            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )

    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


@login_required
def dashboard(request):

    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


@login_required
def edit(request):

    if request.method == 'POST':

        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )

        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

    else:

        user_form = UserEditForm(instance=request.user)

        profile_form = ProfileEditForm(
            instance=request.user.profile
        )

    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

@login_required
def user_follow(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    if request.user != user_to_follow:

        if user_to_follow in request.user.following.all():

            request.user.following.remove(
                user_to_follow
            )

        else:

            request.user.following.add(
                user_to_follow
            )

    return redirect('user_detail',
                    username=username)

from posts.models import Post


def user_detail(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    posts = Post.published.filter(
        user=user
    )

    return render(
        request,
        'account/user/detail.html',
        {
            'user': user,
            'posts': posts
        }
    )