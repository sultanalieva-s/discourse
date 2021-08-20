# Create your views here.
# from rest_framework import filters
from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from main.models import *
from main.serializers import ArticleListSerializer, ArticlePostSerializer, ArticleDetailSerializer, \
    ArticleUpdateSerializer, ArticleCommentListSerializer, ReplyListSerializer, ArticleCommentPostSerializer, \
    ReplyPostSerializer, ArticleLikeSerializer, FavoriteArticlePostSerializer, FavoriteArticleListSerializer, \
    RateSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated, )
    # filterset_fields = ['created', ]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', ]
    ordering = ['created', ]

    def get_serializer_class(self):
        serializers_actions = {'create': ArticlePostSerializer,
                                'list': ArticleListSerializer,
                                'retrieve':  ArticleDetailSerializer,
                                'update': ArticleUpdateSerializer,
                                'partial_update': ArticleUpdateSerializer,
                               }

        return serializers_actions[self.action]

    @action(detail=True, methods=['post'])
    def rate(self, req, pk=None):
        serializer = RateSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False)
    def get_recommendations(self, req):
        user = req.user
        likes = ArticleLike.objects.filter(author=user)
        liked_articles = [i.article for i in likes]
        categories = []

        for i in liked_articles:
            a = Article_ArticleCategory.objects.filter(article=i)
            for k in a:
                categories.append(k.article_category)

        print(categories)

        recommendations = []

        for category in categories:
            articles = Article_ArticleCategory.objects.filter(article_category=category)

            for a in articles:
                recommendations.append(a.article)

        print(recommendations)
        recommendations = set(recommendations)
        recommendations = list(recommendations)
        serializer = ArticleListSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def filter(self, req):
        category = req.query_params.get('category')
        cat_obj = ArticleCategory.objects.get(name=category)
        q = Article_ArticleCategory.objects.filter(article_category=cat_obj)
        articles = []

        for a in q:
            articles.append(a.article)

        serializer = ArticleListSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = Article.objects.all()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(article__icontains=q))
        serializers = ArticleListSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ArticleCommentViewSet(ModelViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializers_actions = {'create': ArticleCommentPostSerializer,
                                'list': ArticleCommentListSerializer,
                                'retrieve':  ArticleCommentListSerializer,
                                'update': ArticleCommentListSerializer,
                                'partial_update': ArticleCommentListSerializer,
                               }

        return serializers_actions[self.action]


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplyListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializers_actions = {'create': ReplyPostSerializer,
                                'list': ReplyListSerializer,
                                'retrieve':   ReplyListSerializer,
                                'update':  ReplyListSerializer,
                                'partial_update':  ReplyListSerializer,
                               }

        return serializers_actions[self.action]


class ArticleLikeViewSet(ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer
    permission_classes = (IsAuthenticated,)


class FavoriteArticleViewset(mixins.CreateModelMixin, mixins.ListModelMixin,  mixins.DestroyModelMixin, GenericViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticlePostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        q = FavoriteArticle.objects.filter(user=user)
        return q

    def get_serializer_class(self):
        serializers_actions = {'create': FavoriteArticlePostSerializer,
                               'list': FavoriteArticleListSerializer,
                               }

        return serializers_actions[self.action]






