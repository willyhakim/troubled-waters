#rango/models.py
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
	name = models.CharField(max_length=128, unique = True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):      
	    return self.title


class UserProfile(models.Model):
	user = models.OneToOneField(User)

	#Additional attributes we wish to include
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	skype = models.CharField(max_length=128, blank=True)

	def __unicode__(self):
		return self.username