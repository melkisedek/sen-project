from django.conf.urls import url

from .views import BookSearchView

urlpatterns = [
    url(r'^$', BookSearchView.as_view(), name="search"),
]
