from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Author(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Publisher(models.Model):
	"""docstring for Publisher"""
	name = models.CharField(max_length=200)
	address = models.TextField(blank=True)
	def __str__(self):
		return self.name
		

class Book(models.Model):
	name = models.CharField(max_length=200)
	edition = models.SmallIntegerField(default=1)
	authors = models.ManyToManyField(Author, blank=True)
	publisher = models.ManyToManyField(Publisher, blank=True)
	year = models.DateTimeField('year published',
		help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
		blank=True)
	pages = models.IntegerField(default=0)
	isbn_10	= models.IntegerField(default=0,help_text="Do not include dashes")
	isbn_13	= models.IntegerField(default=0,help_text="Do not include dashes")
	description = models.TextField()
	cover_image	= models.ImageField('cover Image',
                                upload_to='cover_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
	date_added = models.DateTimeField(default=datetime.now)	
	def __str__(self):
		if self.edition==1:
			nth="st"
		elif self.edition==2:
			nth="nd"
		elif self.edition==3:
			nth="rd"
		else : nth="th"
		return self.title + ", "+ str(self.edition)+nth + " Edition by " + self.author

	def was_added_recently(self):
		return self.date_added >= timezone.now() - datetime.timedelta(days=30)