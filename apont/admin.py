from django.contrib import admin

from apont import models

# Register your models here.


@admin.register(models.Apont_Type)
class Apont_TypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Motive)
class MotiveAdmin(admin.ModelAdmin):
    ...


@admin.register(models.StopsCategory)
class StopsCategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.StopsMotive)
class StopsMotiveAdmin(admin.ModelAdmin):
    list_display = 'name', 'category',
    ordering = "category",
