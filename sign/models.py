from django.contrib.auth.models import AbstractUser
from django.db import models


LIST_POSITION_WORKER = [
    '866',
    '944',
    '914',
    '916',
    '892',
    '961',
    '601',
    '892',
    '773'
]


class User(AbstractUser):

    class Gender(models.TextChoices):
        MAN = 'MN', 'Мужчина'
        WOMAN = 'WN', 'Женщина'

    class Position(models.TextChoices):
        LOCKSMITH = '866', 'Слесарь' # 'LSM'
        TURNER = '914', 'Токарь' # 'TRN'
        MILLER = '944', 'Фрезеровщик' # 'MLR'
        MASTER = 'MSR', 'Мастер' # 'MSR'
        ENGINEER_PDB = 'EPB', 'Инженер ПДБ' # 'EPB'
        SOLDER = '916', 'Пайщик' # 'SLR'
        WELDER = '892', 'Сварщик' # 'WLR'
        GRINDER = '961', 'Шлифовщик' # 'GRN'
        OPERATOR = '773', 'Оператор ЧПУ' # 'PRM'
        TESTER = '601', 'Испытатель' # 'HRM'

    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=200, blank=False, unique=True, verbose_name='Логин')
    name = models.CharField(max_length=70, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=70, blank=False, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=70, blank=False, verbose_name='Отчество')
    employee_number = models.IntegerField(blank=False, verbose_name='Табельный номер')
    region = models.IntegerField(blank=True, default=1, verbose_name='Участок')
    employee_rank = models.IntegerField(blank=False, default=3, verbose_name='Разряд рабочего')
    position = models.CharField(max_length=3, choices=Position.choices, verbose_name='Профессия')
    birthday = models.DateTimeField(verbose_name='День Рождения')
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.MAN, verbose_name='Пол')
    # salary = models.OneToOneField('sign.CalculatinsOfTheOperatorSalary',
    #                               on_delete=models.SET_NULL,
    #                               null=True, blank=True,
    #                               related_name='user_salary')

    def __str__(self):
        return f'{self.username}'

    def get_full_name(self):
        return f'{self.surname} {self.name[0]}.{self.patronymic[0]}.'


# class CalculatinsOfTheOperatorSalary(models.Model):
#     pass

# class WorkingAtTheMachine(models.Model):
#     """""" #FIXME
#
#     class Machine(models.TextChoices):
#         SMEC_1 = '001', 'Смек 1'
#         SMEC_2 = '002', 'Смек 2 барфидер'
#         SMEC_3 = '003', 'Смек 3'
#         SMEC_4 = '004', 'Смек 4 барфидер'
#         SPINNER_1 = '005', 'Шпинер 1'
#         SPINNER_2 = '006', 'Шпинер 2'
#         HI5000 = '007', 'Малыш'
#
#     date = models.DateField(auto_now_add=True)
#     machine = models.CharField(max_length=3, choices=Machine.choices, verbose_name='Станок')
#     work_time_green = models.FloatField(default=0, null=True, blank=True)
#     barfider = models.BooleanField(default=False)
#     detail = models.ForeignKey('workshop_data.Detail', on_delete=models.SET_NULL, blank=False, null=True)









