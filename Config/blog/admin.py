from django.contrib import admin

from .models import Category, Blog, Comment, Like

# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'created_on',
        # 'updated_on',
        'category',
        'assigned_class',
        'subject',
        'author',
        'title',
        # 'introduction',
        # 'content',
        # 'cover_image',
        # 'cover_image_thumbnail',
        'published',
        'make_public',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'category',
        'assigned_class',
        'subject',
        'author',
        'published',
        'make_public',
    )
    # raw_id_fields = ('liked_by',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'post',
        'author',
        'content',
    )
    list_filter = ('created_on', 'updated_on', 'post', 'author')
    # raw_id_fields = ('liked_by',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'user', 'post')
    list_filter = ('created_on', 'updated_on', 'user', 'post')

