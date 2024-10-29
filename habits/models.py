# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}

# WEEKDAY = [
#             (1, 'Понедельник'),
#             (2, 'Вторник'),
#             (3, 'Среда'),
#             (4, 'Четверг'),
#             (5, 'Пятница'),
#             (6, 'Суббота'),
#             (7, 'Воскресенье'),
#         ]


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Владелец привычки')
    action = models.CharField(max_length=255, verbose_name='Действие')
    location = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', related_name='related_to', on_delete=models.SET_NULL, **NULLABLE,
                                      verbose_name='Связанная привычка')
    # periodicity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], choices=WEEKDAY,
    #                                   verbose_name='Периодичность выполнения')
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность выполнения')
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name='Вознаграждение')
    time_to_complete = models.DurationField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    class Meta:
        verbose_name = 'Привычка',
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.action} at {self.time} in {self.location}'
