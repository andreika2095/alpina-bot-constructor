from rest_framework import serializers
from .models import Bot, Scenario, Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class ScenarioSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scenario
        fields = '__all__'

class BotSerializer(serializers.ModelSerializer):
    scenarios = ScenarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = ['owner']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)