from django.conf.urls import url

from . import views

urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    url(r'^$', views.newly_added, name="newly_added"),
]
