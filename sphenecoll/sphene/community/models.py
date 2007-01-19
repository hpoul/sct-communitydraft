from django.db import models

# Create your models here.

class Group(models.Model):
	name = models.CharField(maxlength = 250)
	longname = models.CharField(maxlength = 250)
	default_theme = models.ForeignKey('Theme', null = True, blank = True)

	def __str__(self):
		return self.name;

	class Admin:
		pass
	

class Theme(models.Model):
	name = models.CharField(maxlength = 250)
	path = models.CharField(maxlength = 250)

	def __str__(self):
		return self.name;

	class Admin:
		pass
