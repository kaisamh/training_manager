# training_app/models.py

from django.db import models
from django.contrib.auth.models import User

class TrainingGroup(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_groups')
    members = models.ManyToManyField(User, related_name='training_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    plan_file = models.FileField(upload_to='training_plans/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.date}"

class Feedback(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    individual_tasks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['training_plan', 'member']

    def __str__(self):
        return f"Feedback for {self.member.username} - {self.training_plan.date}"