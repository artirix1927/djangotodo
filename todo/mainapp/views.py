from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .constants import tasks_fit_without_overflow
from .forms import CreateNewUserForm, CreateNewTaskForm, ChangeTaskForm
from .functions import get_searched_tasks, prepare_view_content, redirect_to_prev_page, \
    render_into_template, \
    get_tasks_to_add, get_filtered_user_tasks
from .models import Task


@login_required(login_url='/login/')
def index(request, filter, load_extra=0):
    content, current_user_all_tasks = prepare_view_content(request)

    tasks_to_display = get_filtered_user_tasks(request, filter)

    content['tasks'] = tasks_to_display[:tasks_fit_without_overflow + load_extra]
    content['task_quantity_for_the_filter'] = tasks_to_display.count()

    content['page_filter'] = filter

    return render(request, 'mainapp/index.html', content)


@login_required(login_url='/login/')
def search_task(request, load_extra=0):
    content = prepare_view_content(request).content
    if request.method == "POST":
        # Make it so after changing task from modal window after searching you still have your searched tasks
        request.session['last_searched'] = request.POST['searched']

    tasks_to_display = get_searched_tasks(request, request.session['last_searched'])
    content['tasks'] = tasks_to_display[:tasks_fit_without_overflow + load_extra]
    content['task_quantity_for_the_filter'] = tasks_to_display.count()

    return render(request, 'mainapp/index.html', content)


def load_more(request):
    if request.method == "POST":
        tasks_to_add = get_tasks_to_add(request)
        return JsonResponse(data={'rendered_templates': render_into_template(request, tasks_to_add),
                                  'tasks': serializers.serialize('json', tasks_to_add),
                                  })


def register(request):
    form = CreateNewUserForm()
    if request.method == "POST":

        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'mainapp/registration_page.html', {'form': form})


def change_task(request):
    if request.method == "POST":
        form = ChangeTaskForm(request.POST)
        if form.is_valid():
            try:
                task = Task.objects.get(id=form.cleaned_data['id'])
                form.cleaned_data.pop('id')
                task.update(**form.cleaned_data)
                return redirect_to_prev_page(request)

            except Exception:
                return HttpResponse("Task has been deleted", status=410)


def create_new_task(request):
    if request.method == "POST":
        form = CreateNewTaskForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect_to_prev_page(request)


class LoginPage(LoginView):
    form_class = AuthenticationForm
    template_name = 'admin/login.html'

    def get_success_url(self):
        return reverse_lazy('redirect-to-main')


def change_starred_state(request, task_pk):
    task = Task.objects.get(user=request.user.usermodel, pk=task_pk)
    task.starred = not task.starred
    task.save()

    return redirect_to_prev_page(request)


def delete_task(request, task_pk):
    task = Task.objects.get(user=request.user.usermodel, pk=task_pk)
    task.delete()

    return redirect_to_prev_page(request)


def logout_view(request):
    logout(request)
    return redirect('login')


def redirect_to_main(request):
    return redirect('main', filter='all')
