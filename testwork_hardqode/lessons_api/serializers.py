from rest_framework import serializers
from .models import Product, Lesson, LessonView


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    lesson_views = LessonViewSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
