from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^listings/', views.index, name="listings_index"),
  url(r'^listing/new', views.new, name="listings_index"),
  url(r'^listing/(?P<pk>[0-9]+)/edit', views.edit, name="listing_edit"),
  url(r'^listing/(?P<pk>[0-9]+)/remove', views.delete, name="listing_delete"),
  url(r'^listing/(?P<pk>[0-9]+)', views.view, name="listing_view"),
]
