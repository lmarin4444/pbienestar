from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from comienza.views import entrar_dupla,entrar_pie, entrar_centro, entrar_secretaria,ver_derivaciones, \
	ver_centro, nosotros,documentos,dupla,convivencia,nosotros_con,listado,equipop,dupla_ficha_derivacion, \
    listado_construccion,encargados,construye,mi_error_404,Planes_externosList,entrar_director, \
    entrar_director_centro,entrar_director_psicosocial,director_error,listado_escuela





urlpatterns = [
    url(r'^entrar_dupla/$',login_required(entrar_dupla), name='entrar_dupla'),  
    url(r'^entrar_director/$',login_required(entrar_director), name='entrar_director'),  
    url(r'^entrar_director_centro/$',login_required(entrar_director_centro), name='entrar_director_centro'),  
    url(r'^director_error/$',login_required(director_error), name='director_error'),  
    
    
    url(r'^entrar_director_psicosocial/$',login_required(entrar_director_psicosocial), name='entrar_director_psicosocial'),  

    url(r'^entrar_pie/$',login_required(entrar_pie), name='entrar_pie'),  
    url(r'^entrar_centro/$',login_required(entrar_centro), name='entrar_centro'),  
    url(r'^entrar_secretaria/$',login_required(entrar_secretaria), name='entrar_secretaria'), 
    url(r'^ver_derivaciones/$',login_required(ver_derivaciones), name='ver_derivaciones'), 
    url(r'^ver_centro/$',login_required(ver_centro), name='ver_centro'),
    url(r'^nosotros/$',nosotros, name='nosotros'),  
    url(r'^documentos/$',documentos, name='documentos'),
    url(r'^dupla/$',dupla, name='dupla'),
    url(r'^convivencia/$',convivencia, name='convivencia'),
    url(r'^nosotros_con/$',nosotros_con, name='nosotros_con'),
    url(r'^listados/$',listado, name='listado'),
    url(r'^equipop/$',equipop, name='equipop'),
    url(r'^construye/$',construye, name='construye'),
    url(r'^mi_error_404/$',mi_error_404, name='mi_error_404'),

   




    url(r'^dupla_ficha_derivacion/$',login_required(dupla_ficha_derivacion), name='dupla_ficha_derivacion'),
    url(r'^listado_construccion/$',login_required(listado_construccion), name='listado_construccion'),
    url(r'^listado_escuela/$',login_required(listado_escuela), name='listado_escuela'),

    url(r'^encargados/$',encargados, name='encargados'),
    url(r'^Planes_externosList', login_required(Planes_externosList), name='Planes_externosList'),
   
   
   
]

