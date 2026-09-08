from django.db import models

class CrashIncident(models.Model):
    incident_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=500)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=255, default='511GA / n8n Webhook')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.incident_id} - {self.title} ({self.location})"

    class Meta:
        ordering = ['-created_at']

class NearbyLocation(models.Model):
    CATEGORY_CHOICES = [
        ('TOWING', 'Tow Yard / Recovery Service'),
        ('HOSPITAL', 'Hospital / Emergency Medical'),
        ('POLICE', 'Police Station / Patrol Precinct'),
        ('REPAIR', 'Auto Repair Shop'),
        ('LEGAL', 'Accident Legal Assistance'),
    ]
    crash = models.ForeignKey(CrashIncident, on_delete=models.CASCADE, related_name='nearby_locations')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    distance_miles = models.FloatField(default=2.5)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=50, default='+1 (404) 555-0199')
    address = models.CharField(max_length=255, default='Georgia, USA')

    def __str__(self):
        return f"{self.name} ({self.category}) - Lat: {self.latitude}, Lon: {self.longitude}"

class AdCampaign(models.Model):
    PLATFORM_CHOICES = [
        ('META', 'Meta (Facebook & Instagram)'),
        ('GOOGLE', 'Google Ads'),
        ('TIKTOK', 'TikTok Ads'),
        ('SNAPCHAT', 'Snapchat Ads'),
    ]
    CTA_CHOICES = [
        ('FORM', 'Fill Lead Contact Form'),
        ('CALL', 'Call Operator Now'),
        ('WEBSITE', 'Visit Assistance Website'),
    ]
    
    crash = models.ForeignKey(CrashIncident, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    name = models.CharField(max_length=255, default='Georgia Crash Rapid Campaign')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='META')
    headline = models.CharField(max_length=255)
    primary_text = models.TextField(default='Emergency Roadside Towing & Hospital Assistance available within 5 miles of Georgia incident.')
    cta_type = models.CharField(max_length=50, choices=CTA_CHOICES, default='FORM')
    media_url = models.URLField(default='https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=800&q=80')
    media_file = models.FileField(upload_to='campaign_media/', null=True, blank=True)
    call_number = models.CharField(max_length=50, default='+1 (404) 555-TOWS')
    form_url = models.URLField(default='http://localhost:8000/lead-form/')
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    target_radius_miles = models.FloatField(default=5.0)
    ab_test_active = models.BooleanField(default=True)
    impressions = models.IntegerField(default=1250)
    clicks = models.IntegerField(default=84)
    leads_count = models.IntegerField(default=6)
    status = models.CharField(max_length=50, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} [{self.platform}] - Incident #{self.crash.incident_id if self.crash else 'Custom'}"

    def get_media(self):
        if self.media_file:
            return self.media_file.url
        return self.media_url

    class Meta:
        ordering = ['-created_at']

class Lead(models.Model):
    campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    service_requested = models.CharField(max_length=255, default='Emergency Towing & Assistance')
    platform_source = models.CharField(max_length=50, default='Meta Ads')
    notes = models.TextField(blank=True, default='Lead generated via Ad Preview interaction')
    status = models.CharField(max_length=50, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead: {self.name} ({self.phone}) - {self.platform_source}"

    class Meta:
        ordering = ['-created_at']

class AutomationRuleLog(models.Model):
    rule_name = models.CharField(max_length=255)
    trigger_reason = models.CharField(max_length=500)
    action_taken = models.TextField()
    campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE, null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rule: {self.rule_name} - {self.executed_at.strftime('%H:%M:%S')}"

    class Meta:
        ordering = ['-executed_at']

class GoogleAdsAccountConfig(models.Model):
    developer_token = models.CharField(max_length=255, default='MOCK_DEV_TOKEN_GA_511_CRASH')
    client_id = models.CharField(max_length=255, blank=True, default='')
    client_secret = models.CharField(max_length=255, blank=True, default='')
    refresh_token = models.CharField(max_length=255, blank=True, default='')
    customer_id = models.CharField(max_length=100, default='987-654-3210')
    is_sandbox = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Ads Config (Customer ID: {self.customer_id}) - Sandbox: {self.is_sandbox}"

class GoogleAdsCampaignSync(models.Model):
    campaign = models.OneToOneField(AdCampaign, on_delete=models.CASCADE, related_name='google_sync')
    google_campaign_id = models.CharField(max_length=100)
    google_ad_group_id = models.CharField(max_length=100)
    bidding_strategy_type = models.CharField(max_length=100, default='MAXIMIZE_CONVERSIONS')
    target_cpa_amount = models.DecimalField(max_digits=8, decimal_places=2, default=15.00)
    gaql_last_query = models.TextField(blank=True, default='SELECT campaign.id, metrics.impressions, metrics.clicks FROM campaign')
    sync_status = models.CharField(max_length=50, default='SYNCED')
    synced_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Ads Sync: Campaign {self.google_campaign_id} ({self.campaign.name})"

