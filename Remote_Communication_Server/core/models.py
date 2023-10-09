from django.db import models
from django.utils import timezone
import uuid

class Attacker(models.Model):
    attacker_ip = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

class Victim(models.Model):
    victim_ip = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    
class Session(models.Model):
    start_timestamp = models.DateTimeField(default=timezone.now)
    session_id = models.UUIDField(default=uuid.uuid4)
    attacker = models.ForeignKey(Attacker,on_delete=models.CASCADE)
    victim = models.ForeignKey(Victim,on_delete=models.CASCADE)
    victim_name = models.CharField(max_length=100,null=True)

class Command(models.Model):
    command_to_exec = models.TextField(null=True)
    command_to_exec_timestamp = models.DateTimeField(default=timezone.now,null=True)

class CommandResult(models.Model):
    command_results = models.TextField(null=True)
    command_results_timestamp = models.DateTimeField(default=timezone.now,null=True)

class Files(models.Model):
    file = models.FileField(upload_to='')
    filename = models.CharField(max_length=255)