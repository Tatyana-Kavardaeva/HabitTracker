from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        """ Проверяет правило заполнения полей 'связанная привычка' и 'вознаграждение' """
        related_habit = data.get('related_habit')
        reward = data.get('reward')

        if related_habit and reward:
            raise serializers.ValidationError(
                "Можно заполнить только одно из полей: 'связанная привычка' или 'вознаграждение'.")

        return data
