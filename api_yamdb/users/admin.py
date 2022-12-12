from django.contrib import admin

from users.models import User


@admin.register(User)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',

    )
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = 'empty'
