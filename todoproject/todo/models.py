from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(
        max_length=200, 
        help_text="Enter the task title")

    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Enter the task description (optional)")

    created_date = models.DateTimeField(
        default=timezone.now, 
        help_text="Date and time when the task was created")

    completed = models.BooleanField(
        default=False, 
        help_text="Whether the task is completed")

    due_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Date when the task is due (optional)")

    priority = models.IntegerField(
        default=1, 
        choices=[
            (1, 'Low'), 
            (2, 'Medium'), 
            (3, 'High')], 
        help_text="Priority of the task (1-3)")
    

    def __str__(self):
        return f"{self.title} ({'Completed' if self.completed else 'Pending'})"
    
    class Meta:
        ordering = ['-priority', '-due_date', '-created_date']