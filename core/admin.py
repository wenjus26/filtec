from django.contrib import admin
from .models import Product, Event, EventImage, ContactSubmission, PartnerApplication

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'rich_description')
    inlines = [EventImageInline]
    ordering = ('-created_at',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    readonly_fields = ('name', 'email', 'phone', 'message', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-submitted_at',)

    # Disable adding/deleting contact submissions to make it read-only
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'city', 'warehouse_exists', 'submitted_at')
    readonly_fields = ('company_name', 'contact_person', 'email', 'phone', 'city', 'warehouse_exists', 'experience', 'message', 'submitted_at')
    list_filter = ('warehouse_exists', 'city')
    search_fields = ('company_name', 'contact_person', 'email', 'phone', 'city')
    ordering = ('-submitted_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
