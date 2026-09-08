from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/webhook/crash/', views.crash_webhook, name='crash_webhook'),
    path('api/campaign/create/', views.create_campaign_api, name='create_campaign_api'),
    path('api/campaign/<int:campaign_id>/', views.campaign_detail_api, name='campaign_detail_api'),
    path('api/lead/submit/', views.submit_lead_api, name='submit_lead_api'),
    path('api/automation/run/', views.run_ad_automation_api, name='run_ad_automation_api'),
    path('api/ab-test/<int:campaign_id>/', views.ab_test_api, name='ab_test_api'),
    path('google-ads/', views.google_ads_dashboard_view, name='google_ads_dashboard'),
    path('api/google-ads/config/', views.google_ads_config_api, name='google_ads_config_api'),
    path('api/google-ads/gaql/', views.google_ads_gaql_api, name='google_ads_gaql_api'),
    path('api/google-ads/deploy/<int:campaign_id>/', views.google_ads_deploy_api, name='google_ads_deploy_api'),
    path('api/google-ads/conversion/<int:lead_id>/', views.google_ads_conversion_api, name='google_ads_conversion_api'),
    path('meta-ads/', views.meta_ads_dashboard_view, name='meta_ads_dashboard'),
    path('api/meta-ads/config/', views.meta_ads_config_api, name='meta_ads_config_api'),
    path('api/meta-ads/insights/', views.meta_ads_insights_api, name='meta_ads_insights_api'),
    path('api/meta-ads/deploy/<int:campaign_id>/', views.meta_ads_deploy_api, name='meta_ads_deploy_api'),
    path('api/meta-ads/capi/<int:lead_id>/', views.meta_ads_capi_api, name='meta_ads_capi_api'),
    path('snapchat-ads/', views.snapchat_ads_dashboard_view, name='snapchat_ads_dashboard'),
    path('api/snapchat-ads/config/', views.snapchat_ads_config_api, name='snapchat_ads_config_api'),
    path('api/snapchat-ads/stats/', views.snapchat_ads_stats_api, name='snapchat_ads_stats_api'),
    path('api/snapchat-ads/deploy/<int:campaign_id>/', views.snapchat_ads_deploy_api, name='snapchat_ads_deploy_api'),
    path('api/snapchat-ads/capi/<int:lead_id>/', views.snapchat_ads_capi_api, name='snapchat_ads_capi_api'),
]
