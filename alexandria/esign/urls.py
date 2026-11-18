from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"signature-requests", views.SignatureRequestViewSet)
r.register(r"signatures", views.SignatureViewSet)
r.register(r"deepsign-service-accounts", views.DeepSignServiceAccountViewSet)

urlpatterns = r.urls + [
    path(
        "deepsign/callback",
        views.DeepSignCallbackView.as_view(),
        name="deepsign-callback",
    ),
]
