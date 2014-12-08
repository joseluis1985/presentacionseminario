from django.conf.urls import patterns, include, url
from .views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto_juego.views.hola', name='hola'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'proyecto_juego.apps.inicio.views.hola', name='hola'),

    url(r'^hola$', 'proyecto_juego.apps.inicio.views.hola', name='hola1'),

    #url(r'^$', 'proyecto_juego.apps.inicio.views.registro', name='registro'),
    #url(r'^$', 'proyecto_juego.apps.inicio.views.hola'),
    
    
    url(r'^registrar/$','proyecto_juego.apps.inicio.views.registrou', name='registrou'),
    url(r'^ingresar/$','proyecto_juego.apps.inicio.views.ingresar', name='ingresar'),
    url(r'^logout/$',logout_view),
    url(r'^perfil/$',perfil),
    url(r'^active/$',user_active_view),
    url(r'^lista/$',inicio_view),
    url(r'^modificar/$',modificar_view),
    url(r'^npass/$',modificar_pass),
    url(r'^chat/$',chat,name='coneccion'),
    

    url(r'^perfil/view/(\d+)/$',ver_perfil, name='ver_perfil_user'),


    url(r'^tema/$',registro_tema, name='temas'),
    url(r'^tema/registro/(\d+)/$',registro_preguntas, name='agregar_pregunta'),
    url(r'^tema/editar/(\d+)/$',ver_preguntas, name='editar_pregunta'),
    url(r'^pregunta/editar/(\d+)/$',editar_pregunta, name='editar_pregunta'),
    url(r'^pregunta/eliminar/(\d+)/$',eliminar_pregunta, name='eliminar_pregunta'),
    #url(r'^registro/pregunta/$',registro_pregunta, name='Pregunta'),
    url(r'^agregar/',agregar, name='agregar_pregunta'),
    
    
)

#http://localhost:8000/


