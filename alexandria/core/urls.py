from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"categories", views.CategoryViewSet)
r.register(r"documents", views.DocumentViewSet)
r.register(r"files", views.FileViewSet)
r.register(r"tags", views.TagViewSet)
r.register(r"marks", views.MarkViewSet)
r.register(r"tagsynonymgroups", views.TagSynonymGroupViewSet)

urlpatterns = r.urls

urlpatterns.append(path("hook", views.hook_view, name="hook"))
