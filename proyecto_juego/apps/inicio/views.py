from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
import datetime
from .forms import *
from models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.backends.db import SessionStore
import pdb


# Create your views here.
def hola(request):	
	#return render_to_response ('base.html',RequestContext(request))
	return render_to_response("base.html",RequestContext(request))
def hola1(request):	
	
	return render_to_response("base1.html",RequestContext(request))


# def registro_usuarios(request):
#   if request.method=="POST":
#   		formulario=UserCreationForm(request.POST)
#		if(formulario.is_valid()):
#			formulario.save()
#			return HttpResponseRedirect("//")
#	
##	formulario=UserCreationForm()
#	return render_to_response("usuario/registro.html",{'formulario':formulario},context_instance=RequestContext(request))



def registrou(request):
	if request.method=='POST':
		formulario=fusuario(request.POST)
		if formulario.is_valid(): 
			nuevo_usuario=request.POST['username']
			formulario.save()
			usuario=User.objects.get(username=nuevo_usuario)
			usuario.is_active=False
			usuario.save()
			perfil=Perfil.objects.create(user=usuario)
			return HttpResponseRedirect('/')
	else:
		formulario=fusuario()

	return render_to_response('usuario/reg.html',{'formulario':formulario},RequestContext(request))
	#datos=usuario.objects.all()	
	#return render_to_response ('base.html',RequestContext(request))
	#return render_to_response("usuario/reg.html",{'datos',datos},context_instance=RequestContext(request))


def inicio_view(request):
	usuarios=User.objects.all()
	usuarios=usuarios.objects.filter(tipo_usuario='publico')
	return render_to_response("usuario/lista.html",{'usuarios':usuarios},RequestContext(request))




def logout_view(request):
	p=SessionStore(session_key=request.session["idkey"])
	p["estado"]="desconectado"
	p["name"]=""
	p.save()
	logout(request)
	return HttpResponseRedirect("/")

def perfil(request):
	return render_to_response("usuario/perfil.html",{},context_instance=RequestContext(request))



def ingresar(request):
	if request.method=='POST':
		formulario=AuthenticationForm(request.POST)
		if request.session['cont']>3:
			formulario2=fcaptcha(request.POST)
			if formulario2.is_valid():
			     pass
			else: 
				datos={'formulario':formulario,'formulario2':formulario2}
				return render_to_response("usuario/ingresar.html",datos,context_instance=RequestContext(request))
		if formulario.is_valid:
			Nick=request.POST["username"]
			password=request.POST["password"]
			#acceso=authenticate(username=usuario,password=clave)
			acceso=authenticate(username=Nick,password=password)
			if acceso is not None:
				if acceso.is_active:
					login(request,acceso)
					p=SessionStore()
					p["name"]=Nick
					p["estado"]="conectado"
					p.save()
					request.session["idkey"]=p.session_key
					request.session["name"]=Nick
					return HttpResponseRedirect('/perfil')
				else: 
					login(request,acceso)
					return HttpResponseRedirect('/active')
			else:
				request.session['cont']=request.session['cont']+1
				aux=request.session['cont']
				estado=True
				mensaje="Error en los datos "+str(aux)
				if aux>3:
					formulario2=fcaptcha()
					datos={'formulario':formulario,'formulario2':formulario2,'estado':estado,'mensaje':mensaje}
				else:

					datos={'formulario':formulario,'estado':estado,'mensaje':mensaje}
				return render_to_response('usuario/ingresar.html',datos,context_instance=RequestContext(request))
	else:
		request.session['cont']=0
		formulario=AuthenticationForm()
	return render_to_response('usuario/ingresar.html',{'formulario':formulario},context_instance=RequestContext(request))

#pagina de inicio del sistema
def ver_perfil(request,id):
	menu=permisos(request)
	usuario=User.objects.get(id=int(id))
	return render_to_response("usuario/lista.html",{'usuario':usuario,'estado':True},RequestContext(request))

def user_active_view(request):
	menu=permisos(request)
	if request.user.is_authenticated():
		usuario=request.user
		if usuario.is_active:
			return HttpResponseRedirect("/perfil")
		else:
			if request.method=="POST":
				u=User.objects.get(username=usuario)
				perfil=Perfil.objects.get(user=u)
				formulario=fperfil(request.POST,request.FILES,instance=perfil)
				if formulario.is_valid():
					formulario.save()
					u.is_active=True
					u.save()
					return HttpResponseRedirect("/perfil")
			else:
				formulario=fperfil()
			return render_to_response("usuario/activar.html",{'formulario':formulario},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/login/")

def modificar_view(request):
	menu=permisos(request)
	u=User.objects.get(username=request.user)
	perfil=Perfil.objects.get(user=u)
	if request.method=="POST":
		formulario=fperfil(request.POST,request.FILES,instance=perfil)
		formulario2=feditar_perfil(request.POST)
		if formulario.is_valid() and formulario2.is_valid():
			email=request.POST['email']
			#contrasena=request.POST['password']
			formulario.save()
			u.email=email
			#u.set_password(contrasena)
			u.save()
		return HttpResponseRedirect("/perfil/")
	else:
		formulario=fperfil(instance=perfil)
		formulario2=feditar_perfil(initial={'email':u.email})
		return render_to_response("usuario/editar_perfil.html",{'formulario':formulario,'formulario2':formulario2},context_instance=RequestContext(request))
def modificar_pass(request):
	menu=permisos(request)
	user=User.objects.get(username=request.user)
	perfil=Perfil.objects.get(user=user)
	if request.method=="POST":
		formulario2=feditar(request.POST)
		if 	formulario2.is_valid():
			contrasena=request.POST['password']
			user.set_password(contrasena)
			user.save()
		return HttpResponseRedirect("/perfil/")	
	else:
		formulario2=feditar(initial=={'contrasena':user.set_password})
		return render_to_response("usuario/editar_perfil.html",{'formulario2':formulario2},context_instance=RequestContext(request))
def registro_tema(request):
	tema=temas.objects.all()
	titulo="Registro de Temas"
	if request.method=="POST":
		formulario=ftema(request.POST)
		if formulario.is_valid():
			formulario.save()
			estado=True
			datos={'titulo':titulo,'formulario':formulario,'estado':estado,'tema':tema}
			return render_to_response("usuario/registro_tema.html",datos,context_instance=RequestContext(request))
	else:
		formulario=ftema()
	datos={'titulo':titulo,'formulario':formulario,'tema':tema}
	return render_to_response("usuario/registro_tema.html",datos,context_instance=RequestContext(request))

def ver_tema(request):
	lista=categorias.objects.all()
def registro_preguntas(request,id):
	tema=temas.objects.get(id=int(id))
	titulo="Registre las respuestas"
	if request.method=="POST":
		formulario=fpregunta(request.POST)
		formulario2=frespuesta(request.POST)
		if formulario.is_valid() and formulario2.is_valid():
			pregunta=formulario.save(commit=False)
			pregunta.tema=tema
			pregunta.save()
			respuesta=formulario2.save(commit=False)
			respuesta.pregunta=pregunta
			respuesta.save()
			estado=True
			formulario=fpregunta()
			datos={'titulo':titulo,'formulario':formulario,'estado':estado,'formulario2':formulario2}
			return render_to_response("usuario/registro_preguntas.html",datos,context_instance=RequestContext(request))
	else:
		formulario=fpregunta()
		formulario2=frespuesta()
	datos={'titulo':titulo,'formulario':formulario,'formulario2':formulario2}
	return render_to_response("usuario/registro_preguntas.html",datos,context_instance=RequestContext(request))

def ver_preguntas(request,id):
	tema=temas.objects.get(id=int(id))
	preguntas=Preguntas.objects.filter(tema=tema)
	datos={'tema':tema,'preguntas':preguntas}
	return render_to_response("usuario/ver_preguntas.html",datos,context_instance=RequestContext(request))

def editar_pregunta(request,id):
	pregunta=Preguntas.objects.get(id=int(id))
	respuesta=respuestas.objects.get(pregunta=pregunta)
	titulo="Editar pregunta"
	titulo2="Editar las respuestas"
	if request.method=="POST":
		formulario=fpregunta(request.POST,instance=pregunta)
		formulario2=frespuesta(request.POST,instance=respuesta)
		if formulario.is_valid() and formulario2.is_valid():
			formulario.save()
			formulario2.save()
			estado=True
			datos={'titulo':titulo,'formulario':formulario,'estado':estado,'titulo2':titulo2,'formulario2':formulario2}
			return render_to_response("usuario/registro_preguntas.html",datos,context_instance=RequestContext(request))
	else:
		formulario=fpregunta(instance=pregunta)
		formulario2=frespuesta(instance=respuesta)
	datos={'titulo':titulo,'titulo2':titulo2,'formulario':formulario,'formulario2':formulario2}
	return render_to_response("usuario/registro_preguntas.html",datos,context_instance=RequestContext(request))

def eliminar_pregunta(request,id):
	pregunta=Preguntas.objects.get(id=int(id))
	id=pregunta.tema.id
	respuesta=respuestas.objects.get(pregunta=pregunta)
	pregunta.delete()
	respuesta.delete()
	return HttpResponseRedirect("/tema/editar/"+str(id)+"/")


def agregar(request):	
	#return render_to_response ('base.html',RequestContext(request))
	return render_to_response("usuario/sesion.html",RequestContext(request))
#def partidaU#(request):
#	idsession=request.session["idkey"]
#3	return HttpResponseRedirect("http://localhost:3000/django/"+idsession)


def chat(request):
	idsession=request.session["idkey"]
	return HttpResponseRedirect("http://localhost:3000/django/"+idsession)