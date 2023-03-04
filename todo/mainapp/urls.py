from django.urls import path

from .views import *

urlpatterns = [
    path('', redirect_to_main, name='redirect-to-main'),
    path('registration/', register, name='register'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-starred-state/<int:task_pk>/', change_starred_state, name='change_starred_state'),
    path('delete-task/<int:task_pk>', delete_task, name='delete_task'),
    path('create-task/', create_new_task, name='create_task'),
    path('change-task/', change_task, name='change_task'),
    path('load_more/', load_more, name='load_more'),
    path('<str:filter>/', index, name='main'),
    path('<str:filter>/<int:load_extra>/', index, name='main'),
    path('search', search_task, name='search'),
    path('search/<int:load_extra>', search_task, name='search'),
]
