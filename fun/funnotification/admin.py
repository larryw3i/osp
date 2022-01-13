from django.contrib import admin
from .models import Fnotification

# Register your models here.



@admin.register(Fnotification)
class FnotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'DOC', 'poster',)
    ordering = ('-DOU',)

    def save_model(self, request, obj, form, change):
        obj.poster = request.user
        return super().save_model(request, obj, form, change)
