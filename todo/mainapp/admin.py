from django.contrib import admin

# Register your models here.
from .models import *


class TaskInline(admin.StackedInline):
    model = Task


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

    list_display_links = ('id', 'user')

    inlines = [TaskInline]

    raw_id_fields = ('user',)
    search_fields = ('user__username', 'user__pk')


class TaskAdmin(admin.ModelAdmin):
    fields = ('user', 'title', 'description', 'create_time', 'deadline_time', 'starred')

    list_display = ('id', 'title', 'create_time', 'deadline_time')

    list_display_links = ('id', 'title')

    search_fields = ('title', 'description')

    readonly_fields = ('create_time',)

    ordering = ('create_time', )

    raw_id_fields = ('user', )


admin.site.register(Task, TaskAdmin)
admin.site.register(UserModel, UserAdmin)
