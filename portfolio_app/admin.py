from django.contrib import admin
# admin.py
from django.contrib import admin
from .models import Skill, Project, ContactMessage, SiteVisit

admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ContactMessage)

@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'visited_at')
    list_filter = ('page', 'visited_at')

# Register your models here.
