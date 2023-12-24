# 133 барфидер
time_1 = 720 # общее время работы оператора за станком
qantity_1 = 140
difficultly_1 = 0.5
salary_1 = time_1 / qantity_1 * difficultly_1
green_time_1 = 720
yellow_time_1 = 0.1
coef_1 = green_time_1 / yellow_time_1
time_detail_1 = 5
time_all_detail_for_day_1 = qantity_1 * time_detail_1 # время работы станка в режиме 'по программе' и 'под нагрузкой' за день
time_off_1 = time_1 - time_all_detail_for_day_1
coef2_1 =  time_all_detail_for_day_1 / time_1 * difficultly_1


time_2 = 480 # 433
qantity_2 = 25
difficultly_2 = 1.3
salary_2 = time_2 / qantity_2 * difficultly_2
green_time_2 = 360
yellow_time_2 = 120
coef_2 = green_time_2 / yellow_time_2
time_detail_2 = 12
time_all_detail_for_day_2 =qantity_2 * time_detail_2
time_off_2 = time_2 - time_all_detail_for_day_2
coef2_2 = time_all_detail_for_day_2 / time_2 * difficultly_2


time_3 = 480 # 133 вторая сторона
qantity_3 = 200
difficultly_3 = 1
salary_3= time_3 / qantity_3 * difficultly_3
green_time_3 = 400
yellow_time_3 = 80
coef_3 = green_time_3 / yellow_time_3
time_detail_3 = 1.7
time_all_detail_for_day_3 = qantity_3 * time_detail_3
time_off_3 = time_3 - time_all_detail_for_day_3
coef2_3 =  time_all_detail_for_day_3 / time_3 * difficultly_3

print()
print("salary_1 - ", round(salary_1, 2))
print('coef', round(coef_1, 2))
print('time_off', time_off_1)
print('coef2', round(coef2_1, 2))
print()

print()
print("salary_2 - ", round(salary_2, 2))
print('coef', round(coef_2, 2))
print('time_off', time_off_2)
print('coef2', round(coef2_2, 2))
print()

print()
print("salary_3 - ", round(salary_3, 2))
print('coef', round(coef_3, 2))
print('time_off', time_off_3)
print('coef2', round(coef2_3, 2))
print()

print()
print((0.98 + 0.88 + 0.95 + 0.94) / 4)
print((0.98 + 0.88 + 0.95 + 0.94 + 0.4) / 4)
print()