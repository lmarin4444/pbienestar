# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from models import Peticion
from sesion.models import sesion
from secretaria.models import agenda,Registro
from secretaria.forms import Formagenda
from bitacora.models import Lista

import datetime

def show_calendar(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = agenda.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by('horario_i') 
    return render(
        request,
        "calendario/calendario.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )

def show_proximo(request,ano=None,mes=None):
    
    4/0
    
    hoy = hoy - timedelta(years=+1)
    print hoy
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))

    peticiones = agenda.objects.filter(Q(fecha__month=1) & Q(fecha__year=hoy.year)).order_by('horario_i') 
    return render(
        request,
        "calendario/calendario.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )


def show_secre(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = agenda.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by('horario_i')  
    return render(
        request,
        "calendario/calendario_secretaria.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )


def show_calendar_personal(request,ano=None,mes=None):

    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = agenda.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)& Q(usuario=request.user)).order_by('horario_i')  
    return render(
        request,
        "calendario/calendario_personal.html",
        {
            'hoy':hoy,
            'peticiones':peticiones, 
            'sig':hoy.replace(month=hoy.month+1 if hoy.month<12 else 12,day=1),
            'ant':hoy.replace(month=hoy.month-1 if hoy.month>1 else 1,day=1),
        },
        )


def buscar_fechas (request,dia,mes):
    
    #group_required = 'puede_administrar_encuestas

    age = agenda.objects.filter(Q(fecha__day=dia) & Q(fecha__month=mes) & Q(usuario=request.user)).order_by('horario_i')  
    print age
    context = {
        "agenda":age,
        
         }
    return render(request, 'calendario/calendario_dia.html', context)  

def show_secretaria_mes(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    
    peticiones = agenda.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by('horario_i') 
    return render(
        request,
        "calendario/calendario_secretaria_mes.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'anio':hoy.year,
        }
        )

def show_secretaria_semana(request,ano=None,mes=None):
    hoy = datetime.date.today() if ano is None and mes is None else datetime.date(year=int(ano),month=int(mes),day=1)
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    #peticiones = Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year))) if request.user.is_superuser else Peticion.objects.filter((Q(creado_fecha__month=hoy.month) | Q(inicio_fecha__month=hoy.month) | Q(terminado_fecha__month=hoy.month) | Q(completo_fecha__month=hoy.month)), (Q(asignado_a=request.user)|Q(creado_por=request.user)), (Q(creado_fecha__year=hoy.year) | Q(inicio_fecha__year=hoy.year) | Q(terminado_fecha__year=hoy.year) | Q(completo_fecha__year=hoy.year)))
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(4)
  
    peticiones = agenda.objects.filter(fecha__range=[start_week, end_week]).order_by('fecha')
    
    #peticiones = agenda.objects.filter(Q(fecha__month=hoy.month) & Q(fecha__year=hoy.year)).order_by('horario_i') 
    return render(
        request,
        "calendario/calendario_secretaria_semana.html",
        {
            'hoy':hoy,
            'peticiones':peticiones,
            'anio':hoy.year,
            'start_week':start_week,
            'end_week':end_week,
        }
        )

