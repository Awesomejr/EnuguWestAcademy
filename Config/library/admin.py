from django.contrib import admin

from .models import Category, Book


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'subject',
        'assigned_class',
        'title',
        'author',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'category',
        'subject',
        'assigned_class',
    )