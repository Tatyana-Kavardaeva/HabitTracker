from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Weekday(models.Model):
    day = models.CharField(max_length=20, verbose_name='День недели')
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], unique=True,
                                 verbose_name='Порядковый номер дня в неделе')

    class Meta:
        verbose_name = 'День недели',
        verbose_name_plural = 'Дни недели'

    def __str__(self):
        return self.day


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Владелец привычки')
    action = models.CharField(max_length=255, verbose_name='Действие')
    location = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', related_name='related_to', on_delete=models.SET_NULL, **NULLABLE,
                                      verbose_name='Связанная привычка')
    weekdays = models.ManyToManyField(Weekday, default=1, verbose_name='Дни недели', related_name='habits')
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name='Вознаграждение')
    time_to_complete = models.DurationField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    class Meta:
        verbose_name = 'Привычка',
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.action} at {self.time} in {self.location}'
