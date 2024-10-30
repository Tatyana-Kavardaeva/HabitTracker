from rest_framework import serializers
from habits.models import Habit
from habits.validators import TimeValidator, CustomValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeValidator('time_to_complete'),
            CustomValidator(['related_habit', 'reward', 'pleasant_habit'])
        ]
