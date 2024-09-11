from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Meme, Comment, Profile, MemeEmoji, Retweet  # הוספנו Retweet
from .serializers import MemeSerializer, CommentSerializer
from .forms import CommentForm, MemeForm
import json
from django.contrib.auth import logout, login
from django.db.models import Count


def home_view(request):
    memes = Meme.objects.all().order_by('-created_at')[:10]
    for meme in memes:
        meme.emoji_counts = dict(
            meme.emoji_reactions.values('emoji').annotate(
                count=Count('emoji')).values_list('emoji', 'count'))
        if request.user.is_authenticated:
            user_emoji = meme.emoji_reactions.filter(user=request.user).first()
            meme.user_emoji = user_emoji.emoji if user_emoji else None
    followed_memes = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        followed_users = profile.following.all()
        followed_memes = Meme.objects.filter(
            creator__in=followed_users).order_by('-created_at')[:10]
        for meme in followed_memes:
            meme.emoji_counts = dict(
                meme.emoji_reactions.values('emoji').annotate(
                    count=Count('emoji')).values_list('emoji', 'count'))
            user_emoji = meme.emoji_reactions.filter(user=request.user).first()
            meme.user_emoji = user_emoji.emoji if user_emoji else None
    return render(request, 'home.html', {
        'recent_memes': memes,
        'followed_memes': followed_memes
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # מתחבר את המשתמש אוטומטית
            return redirect('user_profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    user_memes = Meme.objects.filter(
        creator=profile_user).order_by('-created_at')
    is_following = request.user.is_authenticated and request.user.profile.following.filter(
        id=profile_user.id).exists()
    context = {
        'profile_user': profile_user,
        'memes': user_memes,
        'followers_count': profile_user.followers.count(),
        'following_count': profile.following.count(),
        'is_following': is_following,
        'is_own_profile': request.user == profile_user
    }
    return render(request, 'profile.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        if request.user.profile.following.filter(
                id=user_to_follow.id).exists():
            request.user.profile.following.remove(user_to_follow)
        else:
            request.user.profile.following.add(user_to_follow)
    return redirect(
        'user_profile',
        username=username)  # שינינו מ-'profile_view' ל-'user_profile'


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.profile.following.remove(user_to_unfollow)
    return redirect('user_profile', username=username)  # שינינו גם כאן


@login_required
def add_comment(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meme = meme
            comment.save()
    return redirect('meme_detail', meme_id=meme_id)


@login_required
def retweet_meme(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    retweet, created = Retweet.objects.get_or_create(user=request.user,
                                                     meme=meme)
    if not created:
        retweet.delete()
        action = 'removed'
    else:
        action = 'added'
    return JsonResponse({
        'status': 'success',
        'action': action,
        'count': meme.retweets.count()
    })


@login_required
def create_meme(request):
    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.creator = request.user
            meme.save()
            return redirect('meme_detail', meme_id=meme.id)
    else:
        form = MemeForm()
    return render(request, 'create_meme.html', {'form': form})


def meme_detail(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    comments = meme.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    meme.emoji_counts = dict(
        meme.emoji_reactions.values('emoji').annotate(
            count=Count('emoji')).values_list('emoji', 'count'))

    user_emoji = meme.emoji_reactions.filter(
        user=request.user).first() if request.user.is_authenticated else None

    return render(
        request, 'meme_detail.html', {
            'meme': meme,
            'comments': comments,
            'comment_form': comment_form,
            'user_emoji': user_emoji
        })


@login_required
def add_emoji(request, meme_id):
    if request.method == 'POST':
        meme = get_object_or_404(Meme, id=meme_id)
        data = json.loads(request.body)
        emoji = data.get('emoji')
        if emoji:
            reaction, created = MemeEmoji.objects.get_or_create(
                meme=meme, user=request.user, defaults={'emoji': emoji})
            if not created:
                reaction.emoji = emoji
                reaction.save()

            meme.emoji_counts = dict(
                meme.emoji_reactions.values('emoji').annotate(
                    count=Count('emoji')).values_list('emoji', 'count'))
            meme.save()

            return JsonResponse({
                'status': 'success',
                'emoji_counts': meme.emoji_counts
            })
    return JsonResponse({'status': 'error'}, status=400)


class MemeViewSet(viewsets.ModelViewSet):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@login_required
def private_profile(request):
    user = request.user
    memes = Meme.objects.filter(creator=user).order_by('-created_at')
    return render(request, 'private_profile.html', {
        'user': user,
        'memes': memes
    })


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    created_memes = Meme.objects.filter(creator=user,
                                        public=True).order_by('-created_at')
    retweeted_memes = Meme.objects.filter(
        retweets__user=user, public=True).order_by('-retweet__created_at')

    all_memes = list(created_memes) + list(retweeted_memes)
    all_memes.sort(key=lambda x: x.created_at, reverse=True)

    is_following = request.user.is_authenticated and request.user.profile.following.filter(
        id=user.id).exists()

    return render(request, 'public_profile.html', {
        'profile_user': user,
        'all_memes': all_memes,
        'is_following': is_following
    })


def logout_view(request):
    logout(request)
    return redirect('home')
