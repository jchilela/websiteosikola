from django.db import models

# Create your models here.

class Cacesso(models.Model):
	Utilizador = models.CharField(max_length=300)
	Senha = models.CharField(max_length=300)
	def __unicode__(self):
		return unicode(self.Utilizador)