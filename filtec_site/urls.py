from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

# Custom Error Handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # PWA configuration
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest_json'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='service_worker_js'),
    
    # Robots.txt & sitemap.xml for SEO
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    path('sitemap.xml', include('core.urls')), # We can delegate to core.urls or import directly
    
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
