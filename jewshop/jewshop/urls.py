from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include("cart.urls")),
    path('user/', include("users.urls")),
    path('', include("core.urls")),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)