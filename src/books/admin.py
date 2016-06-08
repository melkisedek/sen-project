from django.contrib import admin
from .models import Book, Author, Publisher, Loaned
# Register your models here.
class BookAdmin(admin.ModelAdmin):
	list_display = ('name', 'date_added')
	search_fields = ["name"]
	ordering = ["name"]

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Loaned)