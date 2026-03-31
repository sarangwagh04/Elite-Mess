from django.contrib import admin
from .models import MessMenu, PaymentRequest, Attendance, AttendanceSummary
from django.utils.html import format_html

# Global Admin Header Customization
admin.site.site_header = "EliteMess CMS Control Center"
admin.site.site_title = "EliteMess Admin Portal"
admin.site.index_title = "Welcome to the EliteMess Management Hub"

@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ('day', 'breakfast', 'lunch', 'dinner')
    list_editable = ('breakfast', 'lunch', 'dinner')
    ordering = ('id',)

@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ('student', 'month', 'year', 'total_present_days', 'bill_amount')
    list_filter = ('month', 'year')
    search_fields = ('student__username',)
    readonly_fields = ('bill_amount',)

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'created_at', 'view_screenshot')
    list_filter = ('status', 'created_at')
    search_fields = ('student__username',)
    actions = ['approve_payments', 'reject_payments']

    def view_screenshot(self, obj):
        if obj.screenshot:
            return format_html('<a href="{0}" target="_blank">View Receipt</a>', obj.screenshot.url)
        return "No image"
    view_screenshot.short_description = 'Receipt'

    def approve_payments(self, request, queryset):
        queryset.update(status='PAID')
    approve_payments.short_description = "Mark selected as PAID"

    def reject_payments(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_payments.short_description = "Mark selected as REJECTED"

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    list_filter = ('date', 'is_present')
    search_fields = ('student__username',)
