from rest_framework import serializers

from main.models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('title', )


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class ArticlePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class ArticleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class FavoriteArticleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'






