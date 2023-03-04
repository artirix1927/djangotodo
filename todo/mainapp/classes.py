from typing import TypedDict, NamedTuple
from .forms import CreateNewTaskForm
from django.db.models import QuerySet


class PageMenuContentContainer(TypedDict):
    all_tasks_quantity: int
    starred_quantity: int
    deadline_in_seven_days_quantity: int
    late_tasks_quantity: int
    create_task_form: CreateNewTaskForm


class PreparedViewInfo(NamedTuple):
    content: dict
    current_user_all_tasks: QuerySet
