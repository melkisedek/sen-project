from django.views import generic
from books.models import Book, Loaned
from django.shortcuts import render


class HomePage(generic.TemplateView):

	def get(self, request, *args, **kwargs):
		"""Return the number of Books on the System"""
		count = Book.objects.all().count()
		lcount = Loaned.objects.all().count()
		context = {'count': count,
					'lcount': lcount}
		return render(request, "home.html", context)


class AboutPage(generic.TemplateView):
    template_name = "about.html"
