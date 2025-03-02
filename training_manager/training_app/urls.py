# training_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/add-plan/', views.add_training_plan, name='add_training_plan'),
    path('plan/<int:plan_id>/', views.training_plan_detail, name='training_plan_detail'),
    path('plan/<int:plan_id>/feedback/<int:member_id>/', views.add_feedback, name='add_feedback'),
]