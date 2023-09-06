from django.db import models

class StageName(models.TextChoices):
    EMPTY_VALUE = '', 'Выберите вид работы'
    LOCKSMITH = 'LSM', 'Слесарная'
    TURNER = 'TRN', 'Токарная'
    MILLER = 'MLR', 'Фрезеровочная'
    GRINDER = 'GRN', 'Шлифовальная'
    SOLDERING = 'SLD', 'Пайка'
    PRESS = 'PRS', 'Пресс'
    WELDING = 'WLD', 'Сварка'
    PROGRAM = 'PRM', 'Програмная'
    BURN = 'BRN', 'Прожиг'
    HERMETIC = 'HRM', 'Герметичка'
    CONTROL = 'CTL', 'Контроль'
    THREAD_MILLER = 'TML', 'Резьбо-фрезерная'
    DOVODKA = 'DVD', 'доводка-притирка'