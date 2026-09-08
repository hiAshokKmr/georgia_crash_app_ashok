import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import CrashIncident, NearbyLocation, AdCampaign, Lead

@csrf_exempt
def crash_webhook(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        items = data if isinstance(data, list) else [data]
        
        saved_crashes = 0
        campaigns_created = 0

        for item in items:
            inc_id = item.get('incident_id')
            if not inc_id or inc_id == 'undefined':
                continue

            lat = float(item.get('latitude') or 33.7490)
            lon = float(item.get('longitude') or -84.3880)
            title = item.get('title', 'Georgia Live Crash Alert')
            location = item.get('location', 'Georgia, USA')

            crash, created = CrashIncident.objects.update_or_create(
                incident_id=str(inc_id),
                defaults={
                    'title': title,
                    'location': location,
                    'latitude': lat,
                    'longitude': lon,
                    'description': item.get('description', ''),
                    'source': item.get('source', 'Georgia 511 / n8n Webhook')
                }
            )

            if created:
                saved_crashes += 1

                # Calculate Geo Offsets (approx 1 mile = 0.0145 degrees lat/lon)
                # 1. Tow Yard (approx 1.2 miles away)
                tow_lat = round(lat + random.uniform(-0.015, 0.015), 6)
                tow_lon = round(lon + random.uniform(-0.015, 0.015), 6)
                NearbyLocation.objects.create(
                    crash=crash,
                    name=f"Georgia Express Tow Yard (#{inc_id[-4:]})",
                    category='TOWING',
                    distance_miles=round(random.uniform(0.8, 2.2), 1),
                    latitude=tow_lat,
                    longitude=tow_lon,
                    phone='+1 (404) 555-TOWS',
                    address=f"Corridor near {location}"
                )

                # 2. Nearby Hospital / Emergency Room (approx 2.5 miles away)
                hosp_lat = round(lat + random.uniform(-0.035, 0.035), 6)
                hosp_lon = round(lon + random.uniform(-0.035, 0.035), 6)
                NearbyLocation.objects.create(
                    crash=crash,
                    name="Emory University Hospital Trauma Center",
                    category='HOSPITAL',
                    distance_miles=round(random.uniform(1.8, 4.5), 1),
                    latitude=hosp_lat,
                    longitude=hosp_lon,
                    phone='+1 (404) 555-EMERGENCY',
                    address="Atlanta Metro Health Zone, GA"
                )

                # 3. Nearby Police Station / Georgia State Patrol Precinct
                police_lat = round(lat + random.uniform(-0.025, 0.025), 6)
                police_lon = round(lon + random.uniform(-0.025, 0.025), 6)
                NearbyLocation.objects.create(
                    crash=crash,
                    name="Georgia State Patrol (GSP) Post 48 Precinct",
                    category='POLICE',
                    distance_miles=round(random.uniform(1.1, 3.8), 1),
                    latitude=police_lat,
                    longitude=police_lon,
                    phone='+1 (404) 555-POLICE',
                    address="Public Safety Complex, GA"
                )

                # 4. Auto-spawn 4 Platform Campaigns
                platforms = [
                    ('META', 'Meta (FB/IG)', 'Vehicle Accident on ' + location + '? Get Instant Towing & Support', 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80', 'FORM'),
                    ('GOOGLE', 'Google Ads', 'Need Emergency Towing near ' + location + '? 24/7 Fast Arrival', 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=800&q=80', 'CALL'),
                    ('TIKTOK', 'TikTok Ads', 'Stuck after crash? Fast Towing & Support in Georgia!', 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80', 'FORM'),
                    ('SNAPCHAT', 'Snapchat Ads', 'Emergency Car Towing Georgia - Call Now!', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80', 'CALL')
                ]

                for p_code, p_name, headline, media, cta in platforms:
                    AdCampaign.objects.create(
                        crash=crash,
                        name=f"{p_name} Campaign - {location}",
                        platform=p_code,
                        headline=headline,
                        primary_text=f"Emergency Assistance dispatched for crash on {location}. Click below to connect with local operators immediately.",
                        cta_type=cta,
                        media_url=media,
                        call_number='+1 (404) 555-TOWS',
                        form_url='http://localhost:8000/lead-form/',
                        impressions=random.randint(800, 3500),
                        clicks=random.randint(45, 210),
                        leads_count=random.randint(3, 18),
                        status='ACTIVE'
                    )
                    campaigns_created += 1

        return JsonResponse({
            'status': 'success',
            'message': f'Ingested {len(items)} items',
            'new_crashes': saved_crashes,
            'campaigns_launched': campaigns_created
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def create_campaign_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

    try:
        name = request.POST.get('name', 'Custom Crash Campaign')
        platform = request.POST.get('platform', 'META')
        headline = request.POST.get('headline', 'Georgia Roadside Assistance')
        primary_text = request.POST.get('primary_text', 'Need towing or medical help? Contact our 24/7 hotline.')
        cta_type = request.POST.get('cta_type', 'FORM')
        call_number = request.POST.get('call_number', '+1 (404) 555-0199')
        daily_budget = request.POST.get('daily_budget', 50.00)
        target_radius = request.POST.get('target_radius_miles', 5.0)
        crash_id = request.POST.get('crash_id')

        crash = None
        if crash_id:
            crash = CrashIncident.objects.filter(id=crash_id).first()

        media_file = request.FILES.get('media_file')
        media_url = request.POST.get('media_url') or 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80'

        target_platforms = ['META', 'GOOGLE', 'TIKTOK', 'SNAPCHAT'] if platform == 'ALL' else [platform]

        created_campaigns = []
        for p in target_platforms:
            camp = AdCampaign.objects.create(
                crash=crash,
                name=f"{name} [{p}]",
                platform=p,
                headline=headline,
                primary_text=primary_text,
                cta_type=cta_type,
                media_url=media_url,
                media_file=media_file,
                call_number=call_number,
                daily_budget=daily_budget,
                target_radius_miles=target_radius,
                impressions=random.randint(100, 500),
                clicks=random.randint(10, 50),
                leads_count=0,
                status='ACTIVE'
            )
            created_campaigns.append(camp.id)

        return JsonResponse({
            'status': 'success',
            'message': f'Created {len(created_campaigns)} Campaigns successfully!',
            'campaign_ids': created_campaigns
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def submit_lead_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        campaign_id = data.get('campaign_id')
        name = data.get('name', 'Georgia Driver')
        phone = data.get('phone', '+1 (404) 555-0199')
        email = data.get('email', 'driver@georgia.com')
        service = data.get('service_requested', 'Emergency Towing & Service')
        platform = data.get('platform_source', 'Meta Ads')
        notes = data.get('notes', 'Generated via Interactive Ad Preview')

        campaign = None
        if campaign_id:
            campaign = AdCampaign.objects.filter(id=campaign_id).first()
            if campaign:
                campaign.clicks += 1
                campaign.leads_count += 1
                campaign.save()

        lead = Lead.objects.create(
            campaign=campaign,
            name=name,
            phone=phone,
            email=email,
            service_requested=service,
            platform_source=platform,
            notes=notes,
            status='NEW'
        )

        return JsonResponse({
            'status': 'success',
            'message': f'Lead from {name} stored in Django DB!',
            'lead_id': lead.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def campaign_detail_api(request, campaign_id):
    camp = get_object_or_404(AdCampaign, id=campaign_id)
    return JsonResponse({
        'id': camp.id,
        'name': camp.name,
        'platform': camp.platform,
        'headline': camp.headline,
        'primary_text': camp.primary_text,
        'cta_type': camp.cta_type,
        'media_url': camp.get_media(),
        'call_number': camp.call_number,
        'daily_budget': str(camp.daily_budget),
        'target_radius': camp.target_radius_miles,
        'impressions': camp.impressions,
        'clicks': camp.clicks,
        'leads': camp.leads_count,
        'status': camp.status,
        'location': camp.crash.location if camp.crash else 'Georgia Statewide'
    })

def dashboard_view(request):
    crashes = CrashIncident.objects.prefetch_related('nearby_locations', 'campaigns').all()[:50]
    total_crashes = CrashIncident.objects.count()
    campaigns = AdCampaign.objects.select_related('crash').all()[:50]
    total_campaigns = AdCampaign.objects.count()
    leads = Lead.objects.select_related('campaign').all()[:50]
    total_leads = Lead.objects.count()

    platform_stats = {
        'META': {'impressions': 0, 'clicks': 0, 'leads': 0},
        'GOOGLE': {'impressions': 0, 'clicks': 0, 'leads': 0},
        'TIKTOK': {'impressions': 0, 'clicks': 0, 'leads': 0},
        'SNAPCHAT': {'impressions': 0, 'clicks': 0, 'leads': 0},
    }

    for c in AdCampaign.objects.all():
        if c.platform in platform_stats:
            platform_stats[c.platform]['impressions'] += c.impressions
            platform_stats[c.platform]['clicks'] += c.clicks
            platform_stats[c.platform]['leads'] += c.leads_count

    active_tab = request.GET.get('tab', 'dashboard')

    context = {
        'crashes': crashes,
        'total_crashes': total_crashes,
        'campaigns': campaigns,
        'total_campaigns': total_campaigns,
        'leads': leads,
        'total_leads': total_leads,
        'platform_stats': platform_stats,
        'active_tab': active_tab
    }
    return render(request, 'dashboard.html', context)
