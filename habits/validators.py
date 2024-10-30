from datetime import timedelta
from rest_framework import serializers

from habits.models import Habit


class CustomValidator:
    """ Проверяет правила заполнения полей 'связанная привычка', 'вознаграждение' и 'приятная привычка' """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        pleasant_habit = dict(value).get('pleasant_habit')
        related_habit = dict(value).get('related_habit')
        reward = dict(value).get('reward')

        # Проверяет правило заполнения полей 'связанная привычка' и 'вознаграждение'
        if related_habit and reward:
            raise serializers.ValidationError(
                "Необходимо заполнить только одно из полей: 'связанная привычка' или 'вознаграждение'.")

        # Проверяет признак приятной привычки у связанных привычек
        if related_habit:
            related_habit_instance = Habit.objects.get(pk=related_habit.pk)
            pleasant_habit_instance = related_habit_instance.pleasant_habit
            if pleasant_habit_instance is False:
                raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        # Проверяет наличие полей 'вознаграждение' и 'связанная привычка' у приятной привычки
        if pleasant_habit is True:
            if related_habit is not None or reward is not None:
                raise serializers.ValidationError(
                    "У приятной привычки не должно быть вознаграждения или связанной привычки")


class TimeValidator:
    """ Проверяет время на выполнение привычки на соответствие max значению """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        time = timedelta(seconds=120)
        tmp_val = dict(value).get(self.fields)
        if tmp_val and tmp_val > time:
            raise serializers.ValidationError("Время на выполнение привычки не должно превышать 120 секунд.")


# allow_links = 'youtube.com'
#
#
# def validate_allow_links(value):
#     if allow_links not in value.lower():
#         raise ValidationError('Добавление ссылок на сторонние сайты запрещено')
