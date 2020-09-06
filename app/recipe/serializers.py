from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object"""

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Recipe

        ingredients = serializers.PrimaryKeyRelatedField(
            many=True, queryset=Ingredient.objects.all()
        )
        tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

        fields = (
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "user",
            "tags",
            "ingredients",
        )
        read_only_fields = ("id",)
