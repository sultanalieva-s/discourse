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
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT,  related_name='articles')
    created = models.DateTimeField(auto_now_add=True)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Reply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE)

