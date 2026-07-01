from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('why-us/', views.why_us_view, name='why_us'),
    path('products/', views.products_view, name='products'),
    path('events/', views.events_view, name='events'),
    path('events/<uuid:event_id>/', views.event_detail_view, name='event_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('partner/', views.partner_view, name='partner'),
]
