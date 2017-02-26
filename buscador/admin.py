from django.contrib import admin
from user.models import UserStats

# Register your models here.
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'fh', 'calle1', 'calle2')

admin.site.register(UserStats, UserStatsAdmin)