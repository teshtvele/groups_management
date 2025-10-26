from django.contrib import admin
from .models import Person, PersonGroup, ChangeSet, PersonHistory


@admin.register(PersonGroup)
class PersonGroupAdmin(admin.ModelAdmin):
    list_display = ['id']
    readonly_fields = ['id']


@admin.register(ChangeSet)
class ChangeSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'authored_at', 'author', 'reason']
    list_filter = ['authored_at', 'author']
    readonly_fields = ['id', 'authored_at']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'last_name', 'first_name', 'middle_name', 
        'gender', 'group', 'is_current', 'created_at'
    ]
    list_filter = ['gender', 'is_current', 'created_at']
    search_fields = ['last_name', 'first_name', 'middle_name', 'phone', 'email']
    readonly_fields = ['id', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'middle_name', 'birth_date', 'gender')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Системная информация', {
            'fields': ('group', 'change', 'created_at', 'is_current'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PersonHistory)
class PersonHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'group', 'last_name', 'first_name', 
        'valid_from', 'valid_to'
    ]
    list_filter = ['valid_from', 'valid_to', 'gender']
    search_fields = ['last_name', 'first_name', 'middle_name']
    readonly_fields = ['id']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'middle_name', 'birth_date', 'gender')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Системная информация', {
            'fields': ('group', 'change', 'valid_from', 'valid_to')
        }),
    )
