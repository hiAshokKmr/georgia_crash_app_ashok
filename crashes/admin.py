from django.contrib import admin
from .models import CrashIncident, NearbyLocation, AdCampaign, Lead

class NearbyLocationInline(admin.TabularInline):
    model = NearbyLocation
    extra = 1

class AdCampaignInline(admin.TabularInline):
    model = AdCampaign
    extra = 1

@admin.register(CrashIncident)
class CrashIncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'title', 'location', 'latitude', 'longitude', 'source', 'created_at')
    search_fields = ('title', 'location', 'incident_id')
    inlines = [NearbyLocationInline, AdCampaignInline]

@admin.register(NearbyLocation)
class NearbyLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'distance_miles', 'phone', 'crash')
    list_filter = ('category',)

@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('platform', 'headline', 'crash', 'call_number', 'impressions', 'clicks', 'leads_count', 'status')
    list_filter = ('platform', 'status')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service_requested', 'platform_source', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('platform_source', 'created_at')
