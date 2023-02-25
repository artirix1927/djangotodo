# Create your models here.
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

today = date.today()


# Create your models here.

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_current_user_tasks(request) -> QuerySet:
        return Task.objects.filter(user=request.user.usermodel).order_by('-create_time')

    @classmethod
    def _get_in_seven_days_deadline_tasks(cls, request) -> QuerySet:
        in_seven_days = today + timedelta(days=7)
        deadline_in_seven_days = cls.get_current_user_tasks(request).filter(deadline_time__date__lte=in_seven_days,
                                                                            deadline_time__date__gte=date.today())
        return deadline_in_seven_days

    @classmethod
    def _get_late_tasks(cls, request) -> QuerySet:
        late_tasks = cls.get_current_user_tasks(request).filter(deadline_time__date__lt=today)
        return late_tasks

    @classmethod
    def _get_starred_tasks(cls, request) -> QuerySet:
        return cls.get_current_user_tasks(request).filter(starred=True)

    @classmethod
    def _get_quantity_of_tasks_for_filters(cls, request):
        return cls._get_starred_tasks(request).count(), cls._get_in_seven_days_deadline_tasks(
            request).count(), cls._get_late_tasks(
            request).count()


class Task(models.Model):
    title = models.CharField(max_length=225, db_index=True)
    description = models.CharField(blank=True, max_length=999)
    create_time = models.DateTimeField(auto_now_add=True)
    deadline_time = models.DateTimeField()
    starred = models.BooleanField(default=False)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    def update(self, title, description, deadline_time, starred):
        self.title = title
        self.description = description
        self.deadline_time = deadline_time
        self.starred = starred
        self.save()
