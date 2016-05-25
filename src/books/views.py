from django.shortcuts import get_object_or_404, render
from django.views import generic
from braces.views import LoginRequiredMixin
from .models import Book

# Create your views here.

class ShowNew(LoginRequiredMixin, generic.TemplateView):
	template_name = "books/newly_added.html"
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		recently_added = Book.objects.order_by('date_added')[:5]
		context = {'recently_added': recently_added}
		return render(request, 'books/newly_added.html', context)