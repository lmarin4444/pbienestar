from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from usuario.views import privado,ingresar,cerrar
from django.contrib import admin
from django.contrib.auth.views import login
from usuario.views import RegistroUsuario,ListarUsuario, change_password,Planes_externosEstablecimientoList,\
PlanesExternoEscuelaListView

urlpatterns = [
    
    
   url(r'^privado/$',privado, name='privado'),
   url(r'^ingresar/$',ingresar, name='ingresar'),
   url(r'^cerrar/$', cerrar, name='cerrar'),  

   #url(r'^user/(?P<pk>\d+)/$', UserView.as_view(),name='main_user'),
   #url(r'^entrar$', Login.as_view(), name="login"),
   url(r'^registrar', login_required(RegistroUsuario.as_view()), name="registrar"),
   url(r'^Listar_usuario', login_required(ListarUsuario.as_view()), name="usuario_listar"),
   url(r'^login', login, {'template_name':'index.html'}, name='login'),
   url(r'^password/$', change_password, name='change_password'),
   url(r'^Planes_externosEstablecimientoList/$',login_required(Planes_externosEstablecimientoList), name="Planes_externosEstablecimientoList"),
   # Ver lostado de planes externos 
   url(r'^PlanesExternoEscuelaListView/(?P<pk>\d+)/$',login_required(PlanesExternoEscuelaListView), name='PlanesExternoEscuelaListView'),



   
]
