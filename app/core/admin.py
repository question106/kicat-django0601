from django.contrib import admin
from django.utils.html import format_html
from .models import Award

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'date', 
        'location', 
        'is_active', 
        'display_order',
        'image_preview',
        'created_at'
    ]
    
    list_filter = [
        'is_active', 
        'date', 
        'location',
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'description', 
        'location',
        'short_description'
    ]
    
    list_editable = [
        'is_active', 
        'display_order'
    ]
    
    ordering = ['display_order', '-date']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'description', 'short_description')
        }),
        ('일시 및 장소', {
            'fields': ('date', 'location')
        }),
        ('이미지', {
            'fields': ('image',),
            'description': '권장 크기: 600x400px 이상, 형식: JPG, PNG, WebP'
        }),
        ('표시 설정', {
            'fields': ('is_active', 'display_order'),
            'description': '표시 순서: 낮은 숫자가 먼저 표시됩니다'
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def image_preview(self, obj):
        """Show a small preview of the uploaded image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "이미지 없음"
    image_preview.short_description = "미리보기"
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    
    def save_model(self, request, obj, form, change):
        """Custom save logic if needed"""
        super().save_model(request, obj, form, change)
