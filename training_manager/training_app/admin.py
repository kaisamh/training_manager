# training_app/admin.py
from django.contrib import admin
from .models import TrainingGroup, TrainingPlan, Feedback

admin.site.register(TrainingGroup)
admin.site.register(TrainingPlan)
admin.site.register(Feedback)