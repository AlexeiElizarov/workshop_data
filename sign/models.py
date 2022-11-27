from django.contrib.auth.models import AbstractUser
from django.db import models


LIST_POSITION_WORKER = [
    'LSM',
    'MLR',
    'TRN'
]

class User(AbstractUser):

    class Gender(models.TextChoices):
        MAN = 'MN', 'Мужчина'
        WOMAN = 'WN', 'Женщина'

    class Position(models.TextChoices):
        LOCKSMITH = 'LSM', 'Слесарь'
        TURNER = 'TRN', 'Токарь'
        MILLER = 'MLR', 'Фрезеровщик'
        MASTER = 'MSR', 'Мастер'
        ENGINEER_PDB = 'EPB', 'Инженер ПДБ'

    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=200, blank=False, unique=True)
    name = models.CharField(max_length=70, blank=False)
    surname = models.CharField(max_length=70, blank=False)
    patronymic = models.CharField(max_length=70, blank=False)
    employee_number = models.IntegerField(blank=False)
    employee_rank = models.IntegerField(blank=False, default=3)
    position = models.CharField(max_length=3, choices=Position.choices)
    birthday = models.DateTimeField()
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.MAN)

    def __str__(self):
        return f'{self.username}'

    def get_full_name(self):
        return f'{self.surname} {self.name[0]}.{self.patronymic[0]}.'

# User.add_to_class("__str__", User.add_to_class)