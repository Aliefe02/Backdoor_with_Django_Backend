from rest_framework import serializers
from .models import *


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'

class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = '__all__'

class AttackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attacker
        fields = '__all__'

class CommandResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandResult
        fields = '__all__'

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'
