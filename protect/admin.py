from django.contrib import admin

from workshop_data.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    # prepopulated_fields = {"slug": ("name",)} # автозаполнение поля слаг в админ панели


class DetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefix', 'category')
    exclude = ["balance_semis_in_warehouse", "balance_intermediate_detail_in_warehouse", "parameters_for_spu"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Detail, DetailAdmin)