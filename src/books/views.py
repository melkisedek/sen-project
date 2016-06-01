from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from braces.views import LoginRequiredMixin
from .models import Author, Publisher, Book
from .forms import BookFilterForm


# Create your views here.

class ShowNew(LoginRequiredMixin, generic.TemplateView):
	template_name = "books/newly_added.html"
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		recently_added = Book.objects.order_by('date_added')[:5]
		context = {'recently_added': recently_added}
		return render(request, 'books/newly_added.html', context)

class BookList(LoginRequiredMixin, generic.ListView):
	form_class = BookFilterForm
	template_name = "books/book_list.html"
	paginate_by = 1

	def get(self, request, *args, **kwargs):
		form = self.form_class(data=request.GET)
		qs, facets = self.get_queryset_and_facets(form)
		page = self.get_page(request, qs)
		context = {
			'form': form,
			'facets': facets,
			'object_list': page,
		}
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)

	def get_queryset_and_facets(self, form):
		qs = Book.objects.order_by('name')

		facets = {
			'selected': {},
			'categories': {
				'authors': Author.objects.all(),
				'publishers': Publisher.objects.all(),
				'book': Book.objects.all(),
			},
		}
		if form.is_valid():
			author = form.cleaned_data['author']
			if author:
				facets['selected']['author'] = author
				qs = qs.filter(authors=author).distinct()

			publisher = form.cleaned_data['publisher']
			if publisher:
				facets['selected']['publisher'] = publisher
				qs = qs.filter(publisher=publisher).distinct()

			book = form.cleaned_data['book']
			if book:
				facets['selected']['book'] = book
				qs = qs.filter(books=book).distinct()

		return qs, facets

	def get_page(self, request, qs):
		paginator = Paginator(qs, self.paginate_by)

		page_number = request.GET.get('page')
		try:
			page = paginator.page(page_number)
		except PageNotAnInteger:
			# If page is not an integer, show first page.
			page = paginator.page(1)
		except EmptyPage:
			# If page is out of range, show last existing page.
			page = paginator.page(paginator.num_pages)
		return page

class BookDetail(LoginRequiredMixin, generic.DetailView):
	template_name = "books/book_detail.html"
	context_object_name = 'book_details'
	model = Book