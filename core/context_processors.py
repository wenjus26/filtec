from .models import Catalog

def catalog_processor(request):
    try:
        active_catalog = Catalog.objects.filter(is_active=True).first()
    except Exception:
        active_catalog = None

    default_embed_url = "https://drive.google.com/file/d/1FYIWOf1C1D3GtVpjiKzBV_HQ6pRl0XXV/preview"
    
    if active_catalog and active_catalog.embed_url:
        catalog_url = active_catalog.embed_url
    else:
        # Fallback to embeddable Google Drive Preview URL
        catalog_url = default_embed_url

    return {
        'active_catalog_url': catalog_url,
        'is_fallback_catalog': (catalog_url == default_embed_url)
    }
