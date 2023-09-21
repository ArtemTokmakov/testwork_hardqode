from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    products = models.ManyToManyField(Product)
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title


class LessonView(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_time = models.IntegerField()
    status = models.CharField(max_length=10)

    def set_status(self):
        lesson_duration = self.lesson.duration
        if self.viewed_time >= 0.8 * lesson_duration:
            self.status = "Просмотрено"
        else:
            self.status = "Не просмотрено"
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
