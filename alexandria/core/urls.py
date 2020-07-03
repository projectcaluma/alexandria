from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"categories", views.CategoryViewSet)
r.register(r"documents", views.DocumentViewSet)
r.register(r"files", views.FileViewSet)
r.register(r"tags", views.TagViewSet)

urlpatterns = r.urls
