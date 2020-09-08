from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects fir the current authenticated user only"""

        queryset = self.queryset

        """we might not pass assigned_only get parameter, thats why we are using try catch to get rid of typeError"""
        try:
            assigned_only = bool(int(self.request.query_params.get("assigned_only")))

            if assigned_only:
                # filter those tags/ingredients which are assigned
                queryset = queryset.filter(recipe__isnull=False)
            else:
                # filter those tags/ingredients which are not assigned
                queryset = queryset.filter(recipe__isnull=True)
        except:
            pass

        return queryset.filter(user=self.request.user).order_by("-name").distinct()
        # return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Creates a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseAttrViewSet):
    """Manage ingredient in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrive the queryset for authenticated user"""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset

        if tags:
            tags_id = list(map(int, tags.split(",")))
            queryset = queryset.filter(tags__id__in=tags_id)

        if ingredients:
            ingredients_id = list(map(int, ingredients.split(",")))
            queryset = queryset.filter(ingredients__id__in=ingredients_id)

        return queryset.filter(user=self.request.user)
        # return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return serializer for specific method"""

        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImgaeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Creates recipe detail object"""
        serializer.save(user=self.request.user)

    @action(
        methods=["GET", "POST", "PUT", "DELETE"], detail=True, url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        """upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
