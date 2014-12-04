from django.db import models
from django.contrib.auth.models import User
#from django.db.models import Q
from django.db import connection
from thumbs import ImageWithThumbsField


# Create your models here.
class usuario(models.Model):
	Nick=models.CharField(max_length=100)
	Email=models.EmailField(max_length=100)
	Password=models.CharField(max_length=20)

	def __unicode__(self):
		return "%s "%(self.Nick)


class Perfil(models.Model):	
	user=models.OneToOneField(User,unique=True)
	pais=models.CharField(max_length="30", null=False)
	avatar=ImageWithThumbsField(upload_to="img_user",sizes=((50,50),(200,200)))

class temas(models.Model):
	nombre=models.CharField(max_length=40,unique=True)
	def __str__(self):
		return self.nombre

class Preguntas(models.Model):
	nombre=models.CharField(max_length=500)
	tema=models.ForeignKey(temas)
	def __str__(self):
		return self.nombre

class respuestas(models.Model):
	respuesta_correcta=models.CharField(max_length=600)
	respuesta_opcional=models.CharField(max_length=600)
	respuesta_opciona2=models.CharField(max_length=600)
	respuesta_opciona3=models.CharField(max_length=600)
	pregunta=models.ForeignKey(Preguntas)
	def  __str__(self):



		return self-pregunta
