from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Lesson, LessonView, Product


@api_view(['GET'])
def get_lessons_for_user(request):
    user = request.user
    lessons = Lesson.objects.filter(products__owner=user)
    lesson_data = []

    for lesson in lessons:
        try:
            lesson_view = LessonView.objects.get(lesson=lesson, user=user)
            status = lesson_view.status
            viewed_time = lesson_view.viewed_time
        except LessonView.DoesNotExist:
            status = "Не просмотрено"
            viewed_time = 0

        lesson_data.append({
            'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'status': status,
            'viewed_time': viewed_time
        })

    return Response(lesson_data)


@api_view(['GET'])
def get_lessons_for_product(request, product_id):
    user = request.user
    lessons = Lesson.objects.filter(
        products__owner=user, products__id=product_id
        )
    lesson_data = []

    for lesson in lessons:
        try:
            lesson_view = LessonView.objects.get(lesson=lesson, user=user)
            status = lesson_view.status
            viewed_time = lesson_view.viewed_time
            last_viewed_date = lesson_view.access_date
        except LessonView.DoesNotExist:
            status = "Не просмотрено"
            viewed_time = 0
            last_viewed_date = None

        lesson_data.append({
            'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'status': status,
            'viewed_time': viewed_time,
            'last_viewed_date': last_viewed_date
        })

    return Response(lesson_data)


@api_view(['GET'])
def get_product_statistics(request):
    user = request.user
    products = Product.objects.filter(owner=user)
    statistics = []
    total_users = User.objects.count()

    for product in products:
        lesson_views = LessonView.objects.filter(lesson__products=product)
        total_lessons_viewed = lesson_views.count()
        total_viewing_time = lesson_views.aggregate(
            total_time=Sum('viewed_time'))['total_time']
        total_students = lesson_views.values('user').distinct().count()
        purchase_percentage = (product.accesses.count() / total_users) * 100

        statistics.append({
            'product_id': product.id,
            'product_name': product.name,
            'total_lessons_viewed': total_lessons_viewed,
            'total_viewing_time': total_viewing_time,
            'total_students': total_students,
            'purchase_percentage': purchase_percentage
        })

    return Response(statistics)
