from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path(
        "api/v1/",
        include("alexandria.core.urls"),
    ),
]

if settings.ENABLE_SILK:  # pragma: no cover
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
