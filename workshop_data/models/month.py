from django.db import models


class Month(models.IntegerChoices):
    JANUARY = 1, ('январь')
    FEBRUARY = 2, ('февраль')
    MARCH = 3, ('март')
    APRIL = 4, ('апрель')
    MAY = 5, ('май')
    JUNE = 6, ('июнь')
    JULY = 7, ('июль')
    AUGUST = 8, ('август')
    SEPTEMBER = 9, ('сентябрь')
    OCTOBER = 10, ('октябрь')
    NOVEMBER = 11, ('ноябрь')
    DECEMBER = 12, ('декабрь')
    NOT_SPECIFIED = 13, ('не укзан')