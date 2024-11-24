from django.contrib import admin

from .models import BlogModel, UploadModel


class UploadModelAdmin(admin.ModelAdmin):
    list_filter = (
         "uploaded_at",
         "status",
         "mime_type"
    )
    list_display = ("input_video", "status", "uploaded_at")
    search_fields = (
        "uploaded_at",
        "status",
        "mime_type"
    )




class BlogModelAdmin(admin.ModelAdmin):
    list_filter = (
         "created_at",
    )
    list_display = ("title", "published", "created_at")
    search_fields = (
        "title",
        "text",
        "published",
        "created_at"
    )

    prepopulated_fields = {'slug': ('title', )}


admin.site.register(UploadModel, UploadModelAdmin)
admin.site.register(BlogModel, BlogModelAdmin)
