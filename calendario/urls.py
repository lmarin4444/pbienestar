from django.conf.urls import url
from . import views



urlpatterns = [
   
  
	#path('calendar/<int:ano>/<int:mes>',show_calendar, name='project-admin-show-calendar-ano-mes'),
   
 	url(r'^show/calendar/$',views.show_calendar,name='calendar-ano-mes'),
 	url(r'^show/calendar/$',views.show_proximo,name='calendar-ano-mes-prox'),

 	url(r'^show/calendar/$',views.show_secre,name='calendar-secre'),
 	url(r'^show_secretaria_mes/(?P<ano>\d+)/(?P<mes>\d+)/$',views.show_secretaria_mes,name='show_secretaria_mes'),
 	url(r'^show_secretaria_semana/(?P<ano>\d+)/(?P<mes>\d+)/$',views.show_secretaria_semana,name='show_secretaria_semana'),



    url(r'^show/calendar/(?P<ano>\d+)/(?P<mes>\d+)/$',views.show_calendar,name='calendar2'),
    url(r'^show/calendar/(?P<ano>\d+)/(?P<mes>\d+)/$',views.show_calendar,name='calendar3'),
    
    url(r'^show/calendar$',views.show_calendar_personal,name='personal-ano-mes'),
    url(r'^show/calendar/(?P<ano>\d+)/(?P<mes>\d+)/$',views.show_calendar_personal,name='personal'),

    url(r'^buscar/(?P<dia>\d+)/(?P<mes>\d+)/$',views.buscar_fechas,name='fechas'),

    


	#url(r'^calendario$', views.show_calendar, name='project-admin-show-calendar-ano-mes'),    
	#url(r'^show/calendar$', views.show_calendar, name='project-admin-show-calendar-ano-mes'),    
	#url('calendar/(?P<ano>\d+)/(?P<mes>\d+)/$', views.show_calendar,name='project-admin-show-calendar-ano-mes'),
]
