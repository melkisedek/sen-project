from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from braces.views import LoginRequiredMixin
from .models import Author, Publisher, Book, Loaned
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
	paginate_by = 4

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

class BookDetail(LoginRequiredMixin, generic.DetailView):
	''' Book info should show some loan info.''' 
	template_name = "books/book_detail.html"
	context_object_name = 'book_details'
	model = Book

	def get_context_data(self, **kwargs):
		context = super(BookDetail, self).get_context_data(**kwargs)
		try:
			context['loan'] = Loaned.objects.get(book=self.get_object())
		except (KeyError, Loaned.DoesNotExist):
			context['loan'] = False
		else:
			context['loan'] = True
		return context

class LoanList(LoginRequiredMixin, generic.ListView):
	template_name = "books/loans.html"
	context_object_name = 'loan_list'
	model = Loaned

def loanout(request, book_id):
	b = get_object_or_404(Book, pk=book_id)
	if request.user.is_authenticated and request.user.is_staff:
		try: # If book not in loaned table, add it
			loan = Loaned.objects.get(book=b)
		except (KeyError, Loaned.DoesNotExist):
			loan = Loaned(book=b,loaned_by=request.user)
			loan.save()
			return render_to_response('books/book_detail.html', {
				'book_details': b,
				'messages': 'Success. Please contact secretary to retreave the book'
				}, context_instance=RequestContext(request,
					{ 'loan': 'True',}))
		else:
			return render_to_response('books/book_detail.html', {
				'book_details': b,
				'messages': 'That book is already loaned out.'
				}, context_instance=RequestContext(request,
					{ 'loan': 'True',}))
	else:
		return render_to_response('books/book_details.html', {
				'book_details': b,
				'messages': 'You are not a staff member. Contact administrator'
				}, context_instance=RequestContext(request))

def returnin(request, book_id):
	b = get_object_or_404(Book, pk=book_id)
	if request.user.is_authenticated and request.user.is_staff:
		try: 
			loan = Loaned.objects.get(book=b)
			loan.delete()
			return render_to_response('books/book_detail.html', {
				'book_details': b,
				'messages': 'Success. Please contact secretary to Return the book'
				}, context_instance=RequestContext(request,
					{ 'loan': 'False',}))

		except (KeyError, Loaned.DoesNotExist):
			return render_to_response('books/book_detail.html', {
				'book_details': b,
				'messages': 'Error occured.'
				}, context_instance=RequestContext(request,
					{ 'loan': 'False',}))
	else:
		return render_to_response('books/book_details.html', {
				'book_details': b,
				'messages': 'You are not a staff member. Contact administrator'
				}, context_instance=RequestContext(request))