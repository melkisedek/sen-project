from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from braces.views import LoginRequiredMixin
from books.models import Book, Author, Publisher
from books.forms import BookFilterForm


class BookSearchView(ListView):
	form_class = BookFilterForm
	paginate_by = 10
	template_name = 'search/result.html'

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
		q = self.request.GET.get('q')
		
		#return empty if no query is made
		if q == '' or q == None:
			qs = Book.objects.none()
			facets = {}
			return qs, facets

		qs = Book.objects.filter(
			Q(name__icontains=q) | Q(description__icontains=q)
			).order_by('name')

		#Lookups that span relationships use lowercase
		facets = {
			'selected': {},
			'categories': {
				'authors': Author.objects.filter(book__name__icontains=q),
				'publishers': Publisher.objects.filter(book__name__icontains=q)
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