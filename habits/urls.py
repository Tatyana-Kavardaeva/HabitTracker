from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitDestroyAPIView, \
    HabitUpdateAPIView, PublicHabitListAPIView


app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='habit-list-public'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-retrieve'),
    path('habits/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]
