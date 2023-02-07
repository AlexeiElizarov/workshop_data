from django.db import models

class StageName(models.TextChoices):
    EMPTY_VALUE = '', 'Выберите вид работы'
    LOCKSMITH = 'LSM', 'Слесарый'
    TURNER = 'TRN', 'Токарный'
    MILLER = 'MLR', 'Фрезеровальный'
    GRINDER = 'GRN', 'Шлифовальный'
    SOLDERING = 'SLD', 'Пайка'
    PRESS = 'PRS', 'Пресс'
    WELDING = 'WLD', 'Сварка'
    PROGRAM = 'PRM', 'Програмный'
    BURN = 'BRN', 'Прожиг'
    HERMETIC = 'HRM', 'Герметичка'
    CONTROL = 'CTL', 'Контроль'