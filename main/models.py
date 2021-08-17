from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Discourse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discourses')
    thesis = models.CharField(max_length=255)
    body = models.TextField()


class DiscourseComment(models.Model):
    discourse = models.ForeignKey(Discourse, on_delete=models.CASCADE, related_name='comments')


class ArticleCategory(models.Model):
    slug = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)


class Article(models.Model):
    title = models.CharField(max_length=255)
    article = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    image = models.ImageField(upload_to='articles/images', null=True, blank=True)


class Article_ArticleCategory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    article_category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    created = models.DateTimeField(auto_now_add=True)


class ArticleImage(models.Model):
    image = models.ImageField(upload_to='articles/images')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Reply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes', unique=True)

