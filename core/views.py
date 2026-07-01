from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Event, EventImage, ContactSubmission, PartnerApplication

def home_view(request):
    return render(request, 'index.html', {'active_page': 'home'})

def about_view(request):
    return render(request, 'about.html', {'active_page': 'about'})

def why_us_view(request):
    return render(request, 'why-us.html', {'active_page': 'why_us'})

def products_view(request):
    # Fetch all products from database
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products.html', {
        'active_page': 'products',
        'products': products
    })

def events_view(request):
    # Fetch all events and gallery images
    events = Event.objects.all().order_by('-created_at')
    gallery_images = EventImage.objects.select_related('event').all().order_by('-event__created_at')
    return render(request, 'events.html', {
        'active_page': 'events',
        'events': events,
        'gallery_images': gallery_images
    })

def event_detail_view(request, event_id):
    # Fetch specific event and its images
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {
        'active_page': 'events',
        'event': event
    })

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Save to database
        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        # Support AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been received.'})
            
        messages.success(request, 'Thank you! Your inquiry has been received. Our sales team will get back to you shortly.')
        return redirect('contact')
        
    return render(request, 'contact.html', {'active_page': 'contact'})

def partner_view(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        warehouse_exists_str = request.POST.get('warehouse')
        warehouse_exists = warehouse_exists_str == 'yes'
        experience = request.POST.get('experience')
        message = request.POST.get('message', '')
        
        # Save to database
        app = PartnerApplication.objects.create(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            city=city,
            warehouse_exists=warehouse_exists,
            experience=experience,
            message=message
        )
        
        # Support AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Partner application submitted successfully.'})
            
        messages.success(request, 'Application submitted successfully! We will contact you soon.')
        return redirect('partner')
        
    return render(request, 'partner.html', {'active_page': 'partner'})
