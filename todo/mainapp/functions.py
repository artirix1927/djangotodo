import re

from django.db.models import Q
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string

from .classes import PageMenuContentContainer, PreparedViewInfo
from .constants import tasks_fit_without_overflow
from .forms import ChangeTaskForm, CreateNewTaskForm
from .models import Task
from .models import UserModel

'''another option to make it work, dictionary filter is in constants'''


# def get_filtered_user_tasks(request, filter: str):
#     return filters[filter](request)


def get_filtered_user_tasks(request, filter: str):
    match filter:
        case 'all':
            return UserModel.get_current_user_tasks(request)
        case 'starred':
            return UserModel._get_starred_tasks(request)
        case 'deadline_in_seven_days':
            return UserModel._get_in_seven_days_deadline_tasks(request)
        case 'late':
            return UserModel._get_late_tasks(request)


def get_tasks_to_add(request):
    offset = int(request.POST['offset'])

    if request.POST['page_filter'] == '':
        tasks_to_add = get_searched_tasks(request, request.session['last_searched'])
    else:
        tasks_to_add = get_filtered_user_tasks(request, request.POST['page_filter'])

    tasks_to_add = tasks_to_add[offset: offset + tasks_fit_without_overflow]
    return tasks_to_add


def render_into_template(request, tasks_to_add: QuerySet):
    rendered_templates = []
    for task in tasks_to_add:
        rendered_templates.append(render_to_string('mainapp/task_item.html', {'task': task, 'request': request}))

    return rendered_templates


# better name????
def prepare_view_content(request):
    content = dict()

    current_user_tasks = UserModel.get_current_user_tasks(request)
    content['menu'] = _get_menu_content(request)
    content['form'] = ChangeTaskForm()

    return PreparedViewInfo(content, current_user_tasks)


def get_searched_tasks(request, searched) -> QuerySet:
    searched_for = re.sub(' + ', ' ',
                          searched.strip())  # transforms string so django can correctly filter, cuts spaces and etc

    return UserModel.get_current_user_tasks(request).filter(Q(title__contains=searched_for) | Q(
        description__contains=searched_for))


def redirect_to_prev_page(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def _get_menu_content(request):
    starred_quantity, deadline_in_seven_days_quantity, late_tasks_quantity = \
        UserModel._get_quantity_of_tasks_for_filters(request)

    return PageMenuContentContainer(all_tasks_quantity=UserModel.get_current_user_tasks(request).count(),
                                    starred_quantity=starred_quantity,
                                    deadline_in_seven_days_quantity=deadline_in_seven_days_quantity,
                                    late_tasks_quantity=late_tasks_quantity,
                                    create_task_form=CreateNewTaskForm(),
                                    )
