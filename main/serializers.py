from rest_framework import serializers

from main.models import *
from users.serializers import UserSerializer
User = get_user_model()


class ArticleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleImage
        fields = ('image', )


class ArticleArticleCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='article_category.name')

    class Meta:
        model = Article_ArticleCategory
        fields = ('category_name', )


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = ArticleArticleCategorySerializer(Article_ArticleCategory.objects
                                                                        .filter(article=instance), many=True).data
        representation['author'] = UserSerializer(instance.author).data
        representation['image'] = ArticleImageSerializer(ArticleImage.objects.filter(article=instance).first()).data

        return representation


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'article', 'image', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = ArticleArticleCategorySerializer(Article_ArticleCategory.objects
                                                                        .filter(article=instance), many=True).data
        representation['author'] = UserSerializer(instance.author).data

        representation['images'] = ArticleImageSerializer(ArticleImage.objects.filter(article=instance), many=True).data

        representation['comments'] = ArticleCommentListSerializer(ArticleComment.objects.filter(article=instance), many=True).data

        return representation


# TODO: what to do if a category not in the database
class ArticlePostSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(write_only=True)

    class Meta:
        model = Article
        fields = ('title', 'article', 'categories', )

    def create(self, validated_data):
        req = self.context.get('request')
        # author = req.user

        # TODO: remove when auth is complete
        author = User.objects.first()

        categories = validated_data.pop('categories').split(',')
        images_data = req.FILES

        article = Article.objects.create(author=author,  **validated_data)

        for category in categories:
            category = category.strip()
            try:
                category_obj = ArticleCategory.objects.get(name=category)
            except:
                category_obj = ArticleCategory.objects.create(slug=category, name=category)

            mtm = Article_ArticleCategory.objects.create(article=article, article_category=category_obj)

        for i in images_data.getlist('images'):
            ArticleImage.objects.create(image=i, article=article)

        return article

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = ArticleArticleCategorySerializer(Article_ArticleCategory.objects
                                                                        .filter(article=instance), many=True).data
        representation['author'] = UserSerializer(instance.author).data

        return representation


class ArticleUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(write_only=True)

    class Meta:
        model = Article
        fields = ('title', 'article', 'categories', )

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # setting an authorized user:
        author = User.objects.first()

        categories = validated_data.pop('categories').split(',')

        for k, v in validated_data.items():
            setattr(instance, k, v)

        setattr(instance, 'author', author)

        # resetting categories
        Article_ArticleCategory.objects.filter(article=instance).delete()

        for category in categories:
            category = category.strip()
            try:
                category_obj = ArticleCategory.objects.get(name=category)
            except:
                category_obj = ArticleCategory.objects.create(slug=category, name=category)

            mtm = Article_ArticleCategory.objects.create(article=instance, article_category=category_obj)

        # resetting images
        images_data = request.FILES
        ArticleImage.objects.filter(article=instance).delete()

        for i in images_data.getlist('images'):
            ArticleImage.objects.create(image=i, article=instance)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = ArticleArticleCategorySerializer(Article_ArticleCategory.objects
                                                                        .filter(article=instance), many=True).data
        representation['images'] = ArticleImageSerializer(ArticleImage.objects.filter(article=instance), many=True).data
        return representation


# TODO: add comments, replies
class ArticleCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ('comment', 'article', )

    def create(self, validated_data):
        req = self.context.get('request')
        user = req.user
        temporary = User.objects.first()
        comment = ArticleComment.objects.create(author=temporary, **validated_data)
        return comment


class ArticleCommentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    author_lastname = serializers.CharField(source='author.lastname')

    class Meta:
        model = ArticleComment
        fields = ('comment', 'author', 'author_name', 'author_lastname', 'created')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['replies'] = ReplyListSerializer(Reply.objects.filter(comment=instance), many=True).data
        return repr


class ReplyPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ('comment', 'reply', )

    def create(self, validated_data):
        req = self.context.get('request')
        user = req.user
        temporary = User.objects.first()
        reply = Reply.objects.create(author=temporary, **validated_data)
        return reply


class ReplyListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    author_lastname = serializers.CharField(source='author.lastname')

    class Meta:
        model = Reply
        fields = ('reply', 'author', 'author_name', 'author_lastname', 'created')
