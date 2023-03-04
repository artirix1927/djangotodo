from .models import UserModel

filters = {
    'all': UserModel.get_current_user_tasks,
    'starred': UserModel._get_starred_tasks,
    'late': UserModel._get_late_tasks,
    'deadline_in_seven_days': UserModel._get_in_seven_days_deadline_tasks
}


tasks_fit_without_overflow = 8  # eight tasks fit in my page without html overflow in page

