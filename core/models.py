import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('upvc', 'uPVC Pipes'),
        ('pvc', 'PVC Pipes'),
        ('cpvc', 'CPVC Pipes'),
        ('swr', 'SWR Pipes'),
        ('fittings', 'Ball Valve / Fittings'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text="Detailed description of the product and its applications.")
    image = models.ImageField(upload_to='products/', help_text="Product showcase image.")
    technical_specifications = models.TextField(blank=True, null=True, help_text="Sizing tables or specific technical details.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CATEGORY_CHOICES = [
        ('plumber', 'Mega Plumber Meet'),
        ('dealer', 'Dealer Meet'),
    ]
    
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    main_image = models.ImageField(upload_to='events/main/', help_text="Primary cover image for the event.")
    description = models.TextField(blank=True, null=True, help_text="Short teaser description.")
    rich_description = RichTextUploadingField(help_text="Rich detailed description with uploads.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/gallery/', help_text="Gallery photos linked to this event.")

    def __str__(self):
        return f"Gallery Photo for {self.event.title}"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Submission from {self.name} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"

class PartnerApplication(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    warehouse_exists = models.BooleanField(default=False)
    experience = models.TextField(help_text="Current brands, suppliers, or general industry experience.")
    message = models.TextField(blank=True, null=True, help_text="Additional partner message.")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partner App: {self.company_name} by {self.contact_person}"

class Catalog(models.Model):
    title = models.CharField(max_length=200, default="FILTEC Polyplast Catalog")
    embed_url = models.URLField(
        max_length=1000,
        help_text="OneDrive or Google Drive embed URL. (e.g., https://onedrive.live.com/embed?resid=... or Google Drive preview URL)."
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True, 
        help_text="Set to True to make this the active catalog on the website. Only one should be active at a time."
    )

    def __str__(self):
        return f"{self.title} (Updated: {self.updated_at.strftime('%Y-%m-%d')})"
