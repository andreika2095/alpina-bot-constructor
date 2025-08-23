from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gpt_settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Scenario(models.Model):
    name = models.CharField(max_length=255)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='scenarios')
    initial_step = models.ForeignKey('Step', on_delete=models.SET_NULL, null=True, blank=True, related_name='initial_for_scenarios')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bot.name} - {self.name}"

class Step(models.Model):
    SCREEN_TYPE_CHOICES = [
        ('text', 'Текст'),
        ('input', 'Ввод данных'),
        ('choice', 'Выбор из вариантов'),
    ]
    
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=255)
    screen_type = models.CharField(max_length=20, choices=SCREEN_TYPE_CHOICES, default='text')
    message = models.TextField()
    options = models.JSONField(default=list, blank=True)
    next_step = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_steps')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.scenario.name} - {self.name}"

class UserSession(models.Model):
    user_id = models.CharField(max_length=255)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    current_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_id', 'bot']

    def __str__(self):
        return f"{self.bot.name} - {self.user_id}"