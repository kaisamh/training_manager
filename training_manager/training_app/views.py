# training_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainingGroup, TrainingPlan, Feedback
from .forms import TrainingPlanForm, FeedbackForm, TrainingGroupForm

@login_required
def dashboard(request):
    if request.user.coached_groups.exists():
        # User is a coach
        groups = request.user.coached_groups.all()
        context = {'groups': groups, 'is_coach': True}
    else:
        # User is a member
        groups = request.user.training_groups.all()
        context = {'groups': groups, 'is_coach': False}
    return render(request, 'training_app/dashboard.html', context)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(TrainingGroup, id=group_id)
    training_plans = TrainingPlan.objects.filter(group=group)
    is_coach = request.user == group.coach
    
    context = {
        'group': group,
        'training_plans': training_plans,
        'is_coach': is_coach,
    }
    return render(request, 'training_app/group_detail.html', context)

@login_required
def add_training_plan(request, group_id):
    group = get_object_or_404(TrainingGroup, id=group_id)
    if request.user != group.coach:
        messages.error(request, "Only the coach can add training plans.")
        return redirect('group_detail', group_id=group_id)

    if request.method == 'POST':
        form = TrainingPlanForm(request.POST, request.FILES)
        if form.is_valid():
            training_plan = form.save(commit=False)
            training_plan.group = group
            training_plan.save()
            messages.success(request, "Training plan added successfully.")
            return redirect('group_detail', group_id=group_id)
    else:
        form = TrainingPlanForm()

    return render(request, 'training_app/add_training_plan.html', {'form': form, 'group': group})

@login_required
def add_feedback(request, plan_id, member_id):
    training_plan = get_object_or_404(TrainingPlan, id=plan_id)
    member = get_object_or_404(User, id=member_id)
    
    if request.user != training_plan.group.coach:
        messages.error(request, "Only the coach can add feedback.")
        return redirect('group_detail', group_id=training_plan.group.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.training_plan = training_plan
            feedback.member = member
            feedback.save()
            messages.success(request, "Feedback added successfully.")
            return redirect('training_plan_detail', plan_id=plan_id)
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'training_plan': training_plan,
        'member': member,
    }
    return render(request, 'training_app/add_feedback.html', context)

@login_required
def training_plan_detail(request, plan_id):
    training_plan = get_object_or_404(TrainingPlan, id=plan_id)
    is_coach = request.user == training_plan.group.coach
    feedbacks = Feedback.objects.filter(training_plan=training_plan)
    
    context = {
        'training_plan': training_plan,
        'is_coach': is_coach,
        'feedbacks': feedbacks,
    }
    return render(request, 'training_app/training_plan_detail.html', context)