from django.db import models

from utils.images import resize_image
from utils.model_validator import validate_png

# Create your models here.


class Category(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class MenuLink(models.Model):
    class Meta:
        verbose_name = "Menu Link"
        verbose_name_plural = "Menu Links"

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    site_setup = models.ForeignKey(
        "SiteSetup", on_delete=models.CASCADE, blank=True, null=True
    )  # , related_name='menu')

    def __str__(self):
        return self.text


class SiteSetup(models.Model):
    class Meta:
        verbose_name = "Setup"
        verbose_name_plural = "Setup"

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to="assets/favicon/%Y/%m/",
        blank=True,
        default="",
        validators=[validate_png],
    )
    logo_site = models.ImageField(upload_to="assets/Logo/%Y/%m/", default="")

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        current_logo_img_name = str(self.logo_site.name)

        super().save(*args, **kwargs)
        favicon_changed = False
        logo_site_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if favicon_changed:
            resize_image(self.favicon, 32)

        if self.logo_site:
            logo_site_changed = current_logo_img_name != self.logo_site.name

        if logo_site_changed:
            resize_image(self.logo_site, 150)

    def __str__(self):
        return self.title
