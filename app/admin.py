
from django.contrib import admin
from .models import Post, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'body')
    filter_horizontal = ('tags',)  # To add tags using a multi-select list

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
