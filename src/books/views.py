from django.shortcuts import get_object_or_404, render

from .models import Book

# Create your views here.
def newly_added(request):
	recently_added = Book.objects.order_by('date_added')[:5]
	context = {'recently_added': recently_added}
	return render(request, 'books/newly_added.html', context)
