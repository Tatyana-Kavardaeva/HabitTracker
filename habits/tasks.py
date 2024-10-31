from habits.services import send_telegram_message
from celery import shared_task
from habits.models import Habit
from datetime import datetime, timedelta


@shared_task
def send_message_about_habit():
    """ Отправляет в телеграм напоминание за 5 минут до начала времени выполнения привычки"""
    now = datetime.now()
    current_weekday = now.isoweekday()
    habits = Habit.objects.filter(weekdays__number=current_weekday)

    for habit in habits:
        habit_time = habit.time
        habit_datetime = datetime.combine(datetime.today(), habit_time)

        if habit_datetime - timedelta(minutes=5) <= now <= habit_datetime:
            tg_chat_id = habit.owner.tg_chat_id
            message = f'Я буду {habit.action} в это время: {habit.time} в этом месте: {habit.location}'
            send_telegram_message(chat_id=tg_chat_id, message=message)
