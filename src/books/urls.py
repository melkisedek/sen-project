from django.conf.urls import url

from . import views

urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    url(r'^(?P<pk>[0-9]+)/$', views.BookDetail.as_view(), name="book_detail"),
    url(r'^new/$', views.ShowNew.as_view(), name="newly_added"),
    url(r'^loan/$', views.LoanList.as_view(), name="loan_list)"),
    url(r'^(?P<book_id>\d+)/loanout/$', 'books.views.loanout', name="loanout"),
    url(r'^(?P<book_id>\d+)/returnin/$', 'books.views.returnin', name="returnin"),
    url(r'^$', views.BookList.as_view(), name="book_list"),
]
