from django import template
from mainapp.models import Task

register = template.Library()


@register.inclusion_tag('mainapp/task_item.html')
def display_task_item(task_pk, request):
    task = Task.objects.get(pk=task_pk)
    return {'task': task, 'request': request}


@register.inclusion_tag('mainapp/change_task_window.html')
def display_change_task_window(form):
    return {'form': form}


@register.inclusion_tag('mainapp/create_task_window.html')
def display_create_task_window(form, menu, request):
    return {'form': form, 'menu': menu, 'request': request}


@register.inclusion_tag('mainapp/load_more.html')
def load_more_script(task_quantity_for_the_filter, page_filter):
    return {'task_quantity_for_the_filter': task_quantity_for_the_filter, 'page_filter': page_filter}
