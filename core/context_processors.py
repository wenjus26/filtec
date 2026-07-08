from .models import Catalog

def catalog_processor(request):
    try:
        active_catalog = Catalog.objects.filter(is_active=True).first()
    except Exception:
        active_catalog = None

    # Local static PDF path to bypass cross-origin browser CSP iframe blocking on localhost
    default_embed_url = "/static/test_catalog.pdf"
    
    if active_catalog and active_catalog.embed_url:
        catalog_url = active_catalog.embed_url
    else:
        # Fallback to public test PDF
        catalog_url = default_embed_url

    return {
        'active_catalog_url': catalog_url,
        'is_fallback_catalog': (catalog_url == default_embed_url)
    }
