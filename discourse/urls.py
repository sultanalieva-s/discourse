"""discourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from main.views import ArticleViewSet, ArticleCommentViewSet, ReplyViewSet, ArticleLikeViewSet, FavoriteArticleViewset
from users.views import RegisterView, ActivationView, LoginView, LogoutView, UserViewSet, ForgotPasswordView, \
    CompleteResetPassword

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('articles', ArticleViewSet)
router.register('comments', ArticleCommentViewSet)
router.register('replies', ReplyViewSet)
router.register('likes', ArticleLikeViewSet)
router.register('favorites', FavoriteArticleViewset)

schema_view = get_schema_view(
   openapi.Info(
      title="Discourse API",
      default_version='v1',
      description="Discourse",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="saadatssu@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', CompleteResetPassword.as_view()),
    path('users/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    # path('users/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),

    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),



]
