from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"categories", views.CategoryViewSet)
r.register(r"tags", views.TagViewSet)
r.register(r"documents", views.DocumentViewSet)

urlpatterns = r.urls
