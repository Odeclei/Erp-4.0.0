from django.contrib import admin

from site_setup import models


# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'text',


# @admin.register(models.MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = "text", 'url_or_path',
    search_fields = "text", 'url_or_path',


class MenulinkInline(admin.TabularInline):
    model = models.MenuLink
    extra = 2


@admin.register(models.SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenulinkInline,

    def has_add_permission(self, request):
        return not models.SiteSetup.objects.exists()
