from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/webhook/crash/', views.crash_webhook, name='crash_webhook'),
    path('api/campaign/create/', views.create_campaign_api, name='create_campaign_api'),
    path('api/campaign/<int:campaign_id>/', views.campaign_detail_api, name='campaign_detail_api'),
    path('api/lead/submit/', views.submit_lead_api, name='submit_lead_api'),
]
