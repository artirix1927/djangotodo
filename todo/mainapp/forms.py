from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, UserModel


class DateTimeInputCustom(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 6, 'class': 'form-control'}),
            'deadline_time': DateTimeInputCustom(attrs={'class': 'form-control'}),
            'starred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'user': forms.HiddenInput(),
        }


class ChangeTaskForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_time', 'starred']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 6, 'class': 'form-control'}),
            'deadline_time': DateTimeInputCustom(attrs={'class': 'form-control'}),
            'starred': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class CreateNewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(self.__class__, self).save(commit=False)
        custom_user = UserModel(user=user)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            custom_user.save()
        return user
