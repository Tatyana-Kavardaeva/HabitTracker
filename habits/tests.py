from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Weekday
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Пользователи
        self.user1 = User.objects.create(email='user1@test.pro')
        self.user2 = User.objects.create(email='user2@test.pro')

        # День недели
        self.weekday = Weekday.objects.create(day='Понедельник', number=1)

        # Привычки
        self.habit_u1 = Habit.objects.create(action='habit_1', location='place', time='00:12:00',
                                             owner=self.user1, time_to_complete='00:02:00')
        self.habit_u1.weekdays.add(self.weekday)

        # приятная привычка
        self.habit_u2 = Habit.objects.create(action='habit_2', location='place', time='00:15:00',
                                             owner=self.user2, time_to_complete='00:02:00', pleasant_habit=True)
        self.habit_u2.weekdays.add(self.weekday)

        # опубликованная привычка
        self.habit_is_public = Habit.objects.create(action='habit_3', location='place', time='00:18:00',
                                                    owner=self.user2, is_public=True, time_to_complete='00:02:00')
        self.habit_is_public.weekdays.add(self.weekday)

    def test_habit_retrieve(self):
        """ Проверяет просмотр привычки """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-retrieve', args=(self.habit_u1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get('action'), self.habit_u1.action)

    def test_habit_update(self):
        """ Проверяет обновление привычки """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-update', args=(self.habit_u1.pk,))
        data = {'action': 'update_habit'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), 'update_habit')

    def test_habit_delete(self):
        """ Проверяет удаление привычки  """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-delete', args=(self.habit_u1.pk,))
        response = self.client.delete(url)

        # Проверяем, что ответ имеет статус 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(pk=self.habit_u1.pk)

    def test_habit_list(self):
        """ Проверяет просмотр списка привычек """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        data = response.json()

        # Преобразуем weekdays в список идентификаторов
        weekdays_ids = [self.weekday.pk]

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_u1.pk,
                    "action": self.habit_u1.action,
                    "location": self.habit_u1.location,
                    "time": self.habit_u1.time,
                    "pleasant_habit": self.habit_u1.pleasant_habit,
                    "related_habit": self.habit_u1.related_habit,
                    "weekdays": weekdays_ids,
                    "owner": self.habit_u1.owner.pk,
                    "reward": self.habit_u1.reward,
                    "time_to_complete": self.habit_u1.time_to_complete,
                    "is_public": self.habit_u1.is_public,
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_is_public_list(self):
        """ Проверяет просмотр списка опубликованных привычек """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-list-public')
        response = self.client.get(url)
        data = response.json()

        weekdays_ids = [self.weekday.pk]

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_is_public.pk,
                    "action": self.habit_is_public.action,
                    "location": self.habit_is_public.location,
                    "time": self.habit_is_public.time,
                    "pleasant_habit": self.habit_is_public.pleasant_habit,
                    "related_habit": self.habit_is_public.related_habit,
                    "weekdays": weekdays_ids,
                    "owner": self.habit_is_public.owner.pk,
                    "reward": self.habit_is_public.reward,
                    "time_to_complete": self.habit_is_public.time_to_complete,
                    "is_public": self.habit_is_public.is_public,
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_list_for_unauthorized_user(self):
        """ Проверяет просмотр списка привычек неавторизованным пользователем """

        url = reverse('habits:habit-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data, {'detail': 'Учетные данные не были предоставлены.'})

    def test_habit_is_public_list_for_unauthorized_user(self):
        """ Проверяет просмотр списка опубликованных привычек неавторизованным пользователем """

        url = reverse('habits:habit-list-public')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data, {'detail': 'Учетные данные не были предоставлены.'})

    def test_habit_create(self):
        """ Проверяет создание привычки """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-create')

        weekdays_ids = [self.weekday.pk]

        data = {
            'action': 'new_habit',
            "location": "new_place",
            "time": "12:00:00",
            "time_to_complete": "00:02:00",
            "weekdays": weekdays_ids
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)

    def test_pleasant_habit_create(self):
        """ Проверяет создание приятной привычки """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-create')

        weekdays_ids = [self.weekday.pk]

        data = {
            'action': 'new_habit',
            "location": "new_place",
            "time": "12:00:00",
            "time_to_complete": "00:02:00",
            "weekdays": weekdays_ids,
            "pleasant_habit": True,
            "reward": "test",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У приятной привычки не должно быть вознаграждения или связанной привычки']}
        )

    def test_habit_create_with_reward(self):
        """ Проверяет создание привычки c вознаграждением  """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-create')

        weekdays_ids = [self.weekday.pk]

        data = {
            'action': 'new_habit',
            "location": "new_place",
            "time": "12:00:00",
            "time_to_complete": "00:02:00",
            "weekdays": weekdays_ids,
            "pleasant_habit": False,
            "related_habit": self.habit_u2.pk,
            "reward": "test",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                "Необходимо заполнить только одно из полей: 'связанная привычка' или 'вознаграждение'."]}
        )

    def test_habit_create_with_invalid_related_habit(self):
        """ Проверяет создание привычки c невалидной связанной привычкой  """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-create')

        weekdays_ids = [self.weekday.pk]

        data = {
            'action': 'new_habit',
            "location": "new_place",
            "time": "12:00:00",
            "time_to_complete": "00:02:00",
            "weekdays": weekdays_ids,
            "related_habit": self.habit_u1.pk
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Связанная привычка должна быть приятной.']}
        )

    def test_habit_create_with_invalid_time(self):
        """ Проверяет создание привычки c невалидным временем выполнения  """

        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-create')

        weekdays_ids = [self.weekday.pk]

        data = {
            'action': 'new_habit',
            "location": "new_place",
            "time": "12:00:00",
            "time_to_complete": "00:10:00",
            "weekdays": weekdays_ids
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время на выполнение привычки не должно превышать 120 секунд.']}
        )
