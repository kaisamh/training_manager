# training_app/forms.py

from django import forms
from django.contrib.auth.models import User  # Add this import
from .models import TrainingPlan, Feedback, TrainingGroup

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'rows': 4})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})

class TrainingPlanForm(BaseForm):
    class Meta:
        model = TrainingPlan
        fields = ['date', 'title', 'description', 'plan_file']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class FeedbackForm(BaseForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'individual_tasks']

class TrainingGroupForm(BaseForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = TrainingGroup
        fields = ['name', 'members']