from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meme_app.views import MemeViewSet, CommentViewSet, home_view, register_view, profile_view, add_comment, retweet_meme, meme_detail, create_meme, follow_user, unfollow_user, add_emoji, logout_view, meme_detail  # הוסף את זה בראש הקובץ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'memes', MemeViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='user_profile'),  # שינינו את זה מ-'profile_view' ל-'user_profile'
    path('meme/<int:meme_id>/', meme_detail, name='meme_detail'),
    path('meme/<int:meme_id>/comment/', add_comment, name='add_comment'),
    path('meme/<int:meme_id>/retweet/', retweet_meme, name='retweet_meme'),
    path('meme/<int:meme_id>/emoji/', add_emoji, name='add_emoji'),
    path('create_meme/', create_meme, name='create_meme'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
