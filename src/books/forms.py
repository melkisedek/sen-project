from django import forms
from .models import Author, Publisher, Book 

class BookFilterForm(forms.Form):
	author = forms.ModelChoiceField(
		label="Author",
		required=False,
		queryset=Author.objects.all(),
		)
	publisher = forms.ModelChoiceField(
		label="Publisher",
		required=False,
		queryset=Publisher.objects.all(),
		)
	book = forms.ModelChoiceField(
		label="Book",
		required=False,
		queryset=Book.objects.all(),
		)