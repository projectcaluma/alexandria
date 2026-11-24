from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"signature-requests", views.SignatureRequestViewSet)
r.register(r"signatures", views.SignatureViewSet)

urlpatterns = r.urls
