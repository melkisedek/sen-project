from django.conf.urls import url

from . import views

urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    url(r'^new/$', views.ShowNew.as_view(), name="newly_added"),
]
