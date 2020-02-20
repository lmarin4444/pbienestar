# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.shortcuts import render
from alumno.models import Estudiante
from sesion.models import Intervenidos,objetivo_intervencion,objetivo_intervencionhistoria,Diagnostico, \
	Ficha_de_egreso,Reporte_continuidad
from historia.models import Historia,Ficha_derivacion_historica,Intervenidos_historico,agenda_historica, \
	objetivo_historico, objetivo_intervencion_historico,sesion_historica,Ficha_derivacion_dupla_hostorica, \
	Motivo_Retorno_historia,Diagnostico_historia,Ficha_de_egreso_historia,Reporte_continuidad_historia
from bitacora.models import Lista		
from derivacion.models import Ficha_derivacion,Motivo_Retorno_Ficha_derivacion
from secretaria.models import agenda, Confirma, Registro
from sesion.models import sesion
from sesion.forms import DiagnosticoForm,FichaEgresoForm,ContinuidadForm
from dupla.models import Ficha_derivacion_dupla
import datetime

# Create your views here.

def ir_historia(request,pk):
	dato=Estudiante.objects.get(id=pk)
	context={'dato':dato}
	date = datetime.date.today()
	if request.method=='POST':
		
		try:
			ficha=Ficha_derivacion.objects.get(Estudiante__id=pk,estado=1)
		except Ficha_derivacion.DoesNotExist:
			ficha=""
			
		try:
			objeto=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
			
			
		except objetivo_intervencion.DoesNotExist:
			objeto=None

		
		# primero analizar si hay historia anterior ingresada 	
		#try:
		#	history=Historia.objects.get(Estudiante=dato)
			#history.observacion=history.observacion+"-Con fecha :"+date+"Historia de centro de bienestar"
		#except Historia.DoesNotExist:	
			#history=Historia.objects.create(fecha=date,Estudiante=dato,Ficha_derivacion=ficha,objetivo_intervencion=objeto,observacion="Con fecha :"+date+"Historia desde el centro de bienestar")
		history=Historia.objects.create(fecha=datetime.datetime.now(),Estudiante=dato,Ficha_derivacion=ficha,objetivo_intervencion=objeto,observacion="Con fecha : 13/06/2019 Historia desde el centro de bienestar")	
	#		
	#Todos los datos de la ficha de derivacion
		fecha_derivacion 		=ficha.fecha_derivacion
		pie 					=ficha.pie
		anio_pie				=ficha.anio_pie				
		habilidades				=ficha.habilidades		 	
		cuatro					=ficha.cuatro
		cinco					=ficha.cinco
		conducta				=ficha.conducta 
		rendimiento				=ficha.rendimiento 
		area_responsabilidad	=ficha.area_responsabilidad
		antecedentes_familiares	=ficha.antecedentes_familiares 
		seis					=ficha.seis 
		observacion 			=ficha.observacion 
		
		Red_apoyo 				=ficha.Red_apoyo
		Red_apoyo_obs			=ficha.Red_apoyo_obs
		fecha_espera			=ficha.fecha_espera			

		Ficha_derivacion_historica.objects.create(fecha_derivacion =fecha_derivacion,pie=pie,anio_pie=anio_pie,habilidades=habilidades,
			cuatro=cuatro,cinco=cinco,conducta=conducta,rendimiento=rendimiento,area_responsabilidad=area_responsabilidad,
			antecedentes_familiares=antecedentes_familiares,seis=seis,observacion=observacion,Red_apoyo=Red_apoyo,Red_apoyo_obs=Red_apoyo_obs,
			fecha_espera=fecha_espera,Historia=history)	
		#Los datos del archivo intervenidos
		intervenido=Intervenidos.objects.get(Estudiante__id=pk)
		Intervenidos_historico.objects.create(fecha_intervencion= intervenido.fecha_intervencion,estado = intervenido.estado,
		sintesis= intervenido.sintesis,usuario = intervenido.usuario,fecha_derivacion= intervenido.fecha_derivacion,dia = intervenido.dia,
		mes = intervenido.mes,anno = intervenido.anno,numero = intervenido.numero, activo= intervenido.activo,Profesional = intervenido.Profesional,Historia= history) 	

		#Buscar las intervenciones de ese estudiante
		try:
			
		
				
			agendo=agenda.objects.filter(Estudiante__id=pk)
			
			
			
			for ida in agendo:
				if ida.numero==1 and ida.estado==1:
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',pruebas='',usuario_sesion="",
						situacion='No se reaiza la sesión',obs='',otros='Solo se agendó',obs_confirma='sin confirmación Solo se agendó'
						)
				elif ida.numero==1 and ida.estado==2:
					try:
						confirmacion=Confirma.objects.get(agenda=ida)
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',pruebas='',usuario_sesion="",
						situacion='No se reaiza la sesión',obs='',otros='Solo se agendó',obs_confirma=confirmacion.obs
						)
						confirmacion.delete()
					except Confirma.DoesNotExist:
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',pruebas='',usuario_sesion="",
						situacion='No se reaiza la sesión',obs='',otros='Solo se agendó',obs_confirma='No se realizó confirmación'
						)
						
					
				elif ida.numero==2 and ida.estado==1:
					try:
						Sesion=sesion.objects.get(fecha=ida.fecha,horario_i=ida.horario_i,Estudiante__id=pk)
				
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico=Sesion.publico,privado=Sesion.privado,observacion=Sesion.observacion,
						pruebas=Sesion.pruebas,usuario_sesion=Sesion.usuario.username+" "+Sesion.usuario.first_name+" "+Sesion.usuario.last_name,numero=Sesion.numero,situacion='Asiste a la sesión',obs='',otros='',obs_confirma='No se realiza la confirmación'
						)	
						Sesion.delete()
					except sesion.DoesNotExist:
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario='Sesión sin registo',publico='Sesión sin registo',privado='Sesión sin registo',observacion='Sesión sin registo',
						usuario_sesion='Sesión sin usurio registo',situacion='Sesión sin registo',obs='',otros='',obs_confirma='No se realiza la confirmación'
						)
						
					
				elif ida.numero==2 and ida.estado==2:
					try:
						Sesion=sesion.objects.get(fecha=ida.fecha,horario_i=ida.horario_i,Estudiante__id=pk)
						try:
							confirmacion=Confirma.objects.get(agenda=ida)
						
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
								participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
								usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico=Sesion.publico,privado=Sesion.privado,observacion=Sesion.observacion,
								pruebas=Sesion.pruebas,usuario_sesion=Sesion.usuario.username+" "+Sesion.usuario.first_name+" "+Sesion.usuario.last_name,numero=Sesion.numero,situacion='Asiste a la sesión',obs='',otros='',obs_confirma=confirmacion.obs
								)
							confirmacion.delete()
						
						except Confirma.DoesNotExist:
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
								participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
								usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico=Sesion.publico,privado=Sesion.privado,observacion=Sesion.observacion,
								pruebas=Sesion.pruebas,usuario_sesion=Sesion.usuario.username+" "+Sesion.usuario.first_name+" "+Sesion.usuario.last_name,numero=Sesion.numero,situacion='Asiste a la sesión',obs='',otros='',obs_confirma='No existe registro de confirmación'
								)


						Sesion.delete()
					except sesion.DoesNotExist:
						try:
							confirmacion=Confirma.objects.get(agenda=ida)
						
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
								participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
								usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='Sesión sin registro',privado='Sesión sin registro',observacion='Sesión sin registro',
								usuario_sesion='Sesión sin registro',situacion='Sesión sin registro',obs='',otros='',obs_confirma=confirmacion.obs
								)
							confirmacion.delete()
						
						except Confirma.DoesNotExist:
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
								participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
								usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='Sesión sin registro',privado='Sesión sin registro',observacion='Sesión sin registro',
								usuario_sesion='Sesión sin registro',situacion='Sesión sin registro',obs='',otros='',obs_confirma='Sesión sin registro de confirmación'
								)
						
					
				elif ida.numero==3 and ida.estado==1:
					try:
						registro=Registro.objects.get(agenda=ida)
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
						usuario_sesion="",situacion=registro.situacion,obs=registro.obs,otros=registro.otros,obs_confirma='No se realiza la confirmación'
						)
						registro.delete()	
					except Registro.DoesNotExist:
						agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
						pruebas='',usuario_sesion="",situacion='Sin realización de registro',obs='Sin observación de registro',otros='Sin realización de registro',obs_confirma='No se realiza la confirmación'
						)
												
				elif ida.numero==3 and ida.estado==2:
					try:
						registro=Registro.objects.get(agenda=ida)
						try:
							confirmacion=Confirma.objects.get(agenda=ida)
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
							participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
							usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
							pruebas='',usuario_sesion="",situacion=registro.situacion,obs=registro.obs,otros=registro.otros,obs_confirma=confirmacion.obs
							)
							confirmacion.delete()
						except Confirma.DoesNotExist:
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
							participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
							usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
							usuario_sesion="",situacion=registro.situacion,obs=registro.obs,otros=registro.otros,obs_confirma='Sin registro de confirmación'
							)
						
						registro.delete()
							
					except Registro.DoesNotExist:
						try:
							confirmacion=Confirma.objects.get(agenda=ida)
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
							participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
							usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
							pruebas='',usuario_sesion="",situacion='Sin información de registro',obs='Sin información de registro',otros='Sin información de registro',obs_confirma=confirmacion.obs
							)
							confirmacion.delete()
						except Confirma.DoesNotExist:
							
							agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
							participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
							usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
							pruebas='',usuario_sesion="",situacion='Sin información de registro',obs='Sin información de registro',otros='Sin información de registro',obs_confirma='Sin registro de confirmación'
							)
										
			
		except agenda.DoesNotExist:						
			agendo=None
		#Grabar la derivacion a otra institucion
		try:
			retorno=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=ficha)
			Motivo_Retorno_historia.objects.create(fecha_retorno=retorno.fecha_retorno,
			Historia=history,motivo_termino=retorno.get_motivo_termino(),observacion_termino=retorno.observacion_termino,
			opcion1=retorno.opcion1,filename1=retorno.filename1,docfile1=retorno.docfile1,
			opcion2=retorno.opcion2,filename2=retorno.filename2,docfile2=retorno.docfile2,
			opcion3=retorno.opcion3,filename3=retorno.filename3,docfile3=retorno.docfile3,
			Ficha_derivacion=ficha,Red_apoyo=retorno.Red_apoyo)
			retorno.delete()	

		except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
			retorno=None
			
	#Objetivo de la intervencion

		try:
			objetivo=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
			objetivo_intervencion_historico.objects.create(fecha_creacion=objetivo.fecha_creacion,
			Historia=history,objetivo_particular=objetivo.objetivo_particular,
			#aqui va la asignacion de tematicas que no puedo hacer
			#Tematicas=objetivo.Tematicas.add(objetivo.Tematicas),usuario=objetivo.usuario)
			#Tematicas= objetivo.Tematicas.all(),	
			usuario=objetivo.usuario)

			#Buscar el objetivo recien creado
			objeto.activo=2
			objeto.save()
			
		
			
		except objetivo_intervencion.DoesNotExist:
			
			objetivo_intervencion_historico.objects.create(fecha_creacion=datetime.date.today(),
			Historia=history,objetivo_particular='Estudiante sin asignación de objetivo',
			#aqui va la asignacion de tematicas que no puedo hacer
			#Tematicas=objetivo.Tematicas.add(objetivo.Tematicas),usuario=objetivo.usuario)
			usuario=request.user)
			objetivo= None
		#Borrar los objetivos de intervencion historica 
		
		try:
			objetivo_his=objetivo_intervencionhistoria.objects.filter(Estudiante__id=pk)
			objetivo_his.delete()
		except objetivo_intervencionhistoria.DoesNotExist:
			obje=None	

		try:
			evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
			Diagnostico_historia.objects.create(Historia=history,fecha=evaluacion.fecha,
			situacion_actual=evaluacion.situacion_actual,observaciones=evaluacion.observaciones,
			familia=evaluacion.familia,usuario=evaluacion.usuario)
			evaluacion.delete()	

		#Borrar los objetivos de intervencion historica 
		except Diagnostico.DoesNotExist:
			evaluacion=None
			#Diagnostico_historia.objects.create(Historia=history,fecha=datetime.date.today(),
			#situacion_actual='sin registro',observacion='sin observación',familia='sin sugerencias',usuario=None)

		try:
			salir=Ficha_de_egreso.objects.get(Estudiante__id=pk)
			Ficha_de_egreso_historia.objects.create(Historia=history,fecha_informe=salir.fecha,
			fecha_egreso=salir.fecha_egreso,Motivo_egreso=salir.Motivo_egreso,sintesis=salir.sintesis,
			sugerencias=salir.sugerencias,usuario=salir.usuario)
			salir.delete()
	

		#Borrar los objetivos de intervencion historica 
		except Ficha_de_egreso.DoesNotExist:
			salir=None

		try:
			continuidad=Reporte_continuidad.objects.filter(Estudiante__id=pk)
			for continuo in continuidad.all():
				Reporte_continuidad_historia.objects.create(Historia=history,fecha=continuo.fecha,
					motivo=continuo.motivo,antecedentes=continuo.antecedentes,observaciones=continuo.observaciones,
					sugerencias=continuo.sugerencias,usuario=continuo.usuario)
				continuo.delete()	
		except Reporte_continuidad.DoesNotExist:
			continuidad=None
	
		ficha.estado=2
		ficha.save()
		#Borrra retorno a una institucion y lo graba en historia
		intervenido.delete()
		agendo.delete()
		

		return redirect('derivacion:intervencion_listar')
	
		
	return render(request,"historia/aviso_termino.html",context)	
	

# -------------------- Historia de un caso dentro de la dupla 
def ir_historia_dupla(request,pk):
	dato=Estudiante.objects.get(id=pk)
	escuela=dato.curso.establecimiento
	context={'dato':dato,
			'escuela':escuela}
	
	if request.method=='POST':
		date = datetime.date.today()
		
		
		try:
			ficha=Ficha_derivacion_dupla.objects.get(Estudiante__id=pk,estado=1)
		except Ficha_derivacion_dupla.DoesNotExist:
			ficha=None
			
		

		history=Ficha_derivacion_dupla_hostorica.objects.create(fecha=date,Estudiante=dato,Ficha_derivacion=ficha,objetivo_intervencion=objeto,observacion="Información desde la dupla PsicoSocial")
		

	#Todos los datos de la ficha de derivacion del area PsicoSocial



		fecha_derivacion 		=ficha.fecha_derivacion
		quien_deriva			=ficha.quien_deriva
		profe_jefe				=ficha.profe_jefe				
		
		conducta				=ficha.conducta
		afecta					=afecta.cinco
		reiterada				=ficha.reiterada 
		marzo					=ficha.marzo 	
		abril					=ficha.abril 	
		mayo					=ficha.mayo 	
		junio					=ficha.junio 	
		julio					=ficha.julio 	
		agosto					=ficha.agosto 	
		septiembre				=ficha.septiembre 	
		octubre					=ficha.octubre 	
		noviembre				=ficha.noviembre 	
		diciembre				=ficha.diciembre 	
		observacion	  			=ficha.observacion
		establecimiento 		= ficha.establecimiento 
		curso 					= ficha.curso 
		letra 					= ficha.letra 
		estudiante 				= ficha.estudiante
		edad 					= ficha.edad
		edad_f  				= ficha.edad_f
		usuario  				= ficha.user

		

		Ficha_derivacion_dupla_historica.objects.create(fecha_derivacion =fecha_derivacion,pie=pie,anio_pie=anio_pie,habilidades=habilidades,
			cuatro=cuatro,cinco=cinco,conducta=conducta,rendimiento=rendimiento,area_responsabilidad=area_responsabilidad,
			antecedentes_familiares=antecedentes_familiares,seis=seis,observacion=observacion,Red_apoyo=Red_apoyo,Red_apoyo_obs=Red_apoyo_obs,
			fecha_espera=fecha_espera,Historia=history)	
		
		#Buscar las intervenciones de ese estudiante
		try:
			
		
			agendo=agenda.objects.filter(Estudiante__id=pk)
			for ida in agendo:
				if ida.numero==1 and ida.estado==1:
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',pruebas='',usuario_sesion="",
						situacion='No se reaiza la sesión',obs='',otros='Solo se agendó',obs_confirma='sin confirmación Solo se agendó'
						)
				elif ida.numero==1 and ida.estado==2:
					confirmacion=Confirma.objects.get(agenda=ida)
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',pruebas='',usuario_sesion="",
						situacion='No se reaiza la sesión',obs='',otros='Solo se agendó',obs_confirma=confirmacion.obs
						)
					confirmacion.delete()
				elif ida.numero==2 and ida.estado==1:
					Sesion=sesion.objects.get(fecha=ida.fecha,horario_i=ida.horario_i,Estudiante__id=pk)
				
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico=Sesion.publico,privado=Sesion.privado,observacion=Sesion.observacion,
						pruebas=Sesion.pruebas,usuario_sesion=Sesion.usuario.username+" "+Sesion.usuario.first_name+" "+Sesion.usuario.last_name,numero=Sesion.numero,situacion='Asiste a la sesión',obs='',otros='',obs_confirma='No se realiza la confirmación'
						)	
					Sesion.delete()
				elif ida.numero==2 and ida.estado==2:
					Sesion=sesion.objects.get(fecha=ida.fecha,horario_i=ida.horario_i,Estudiante__id=pk)
					confirmacion=Confirma.objects.get(agenda=ida)
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico=Sesion.publico,privado=Sesion.privado,observacion=Sesion.observacion,
						pruebas=Sesion.pruebas,usuario_sesion=Sesion.usuario.username+" "+Sesion.usuario.first_name+" "+Sesion.usuario.last_name,numero=Sesion.numero,situacion='Asiste a la sesión',obs='',otros='',obs_confirma=confirmacion.obs
						)
					confirmacion.delete()
					Sesion.delete()
				elif ida.numero==3 and ida.estado==1:
					registro=Registro.objects.get(agenda=ida)
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
						pruebas='',usuario_sesion="",situacion=registro.situacion,obs=registro.obs,otros=registro.otros,obs_confirma='No se realiza la confirmación'
						)
					registro.delete()								
				elif ida.numero==3 and ida.estado==2:
					registro=Registro.objects.get(agenda=ida)
					confirmacion=Confirma.objects.get(agenda=ida)
					agenda_historica.objects.create(fecha=ida.fecha,Historia=history,horario_i=ida.horario_i,
						participantes=ida.participantes,tipo_sesion=ida.tipo_actividad,
						usuario=ida.usuario.username+" "+ida.usuario.first_name+" "+ida.usuario.last_name,publico='NO SE REALIZÓ LA SESIÓN',privado='-',observacion='-',
						pruebas='',usuario_sesion="",situacion=registro.situacion,obs=registro.obs,otros=registro.otros,obs_confirma=confirmacion.obs
						)
					registro.delete()
					confirmacion.delete()						
			
		except agenda.DoesNotExist:						
			agendo=None
		#Grabar la derivacion a otra institucion
		try:
			retorno=Motivo_Retorno_Ficha_derivacion.objects.get(Ficha_derivacion=ficha)
			Motivo_Retorno_historia.objects.create(fecha_retorno=retorno.fecha_retorno,
			Historia=history,motivo_termino=retorno.get_motivo_termino(),observacion_termino=retorno.observacion_termino,
			opcion1=retorno.opcion1,filename1=retorno.filename1,docfile1=retorno.docfile1,
			opcion2=retorno.opcion2,filename2=retorno.filename2,docfile2=retorno.docfile2,
			opcion3=retorno.opcion3,filename3=retorno.filename3,docfile3=retorno.docfile3,
			Ficha_derivacion=ficha,Red_apoyo=retorno.Red_apoyo)
			retorno.delete()	

		except Motivo_Retorno_Ficha_derivacion.DoesNotExist:
			retorno=None
			
	#Objetivo de la intervencion

		try:
			objetivo=objetivo_intervencion.objects.get(Estudiante__id=pk,activo=1)
			objetivo_intervencion_historico.objects.create(fecha_creacion=objetivo.fecha_creacion,
			Historia=history,objetivo_particular=objetivo.objetivo_particular,
			#aqui va la asignacion de tematicas que no puedo hacer
			#Tematicas=objetivo.Tematicas.add(objetivo.Tematicas),usuario=objetivo.usuario)
			#Tematicas= objetivo.Tematicas.all(),	
			usuario=objetivo.usuario)

			#Buscar el objetivo recien creado
			objeto.activo=2
			objeto.save()
			
		
			
		except objetivo_intervencion.DoesNotExist:
			
			objetivo_intervencion_historico.objects.create(fecha_creacion=datetime.date.today(),
			Historia=history,objetivo_particular='Estudiante sin asignación de objetivo',
			#aqui va la asignacion de tematicas que no puedo hacer
			#Tematicas=objetivo.Tematicas.add(objetivo.Tematicas),usuario=objetivo.usuario)
			usuario=request.user)
			objetivo= None
		#Borrar los objetivos de intervencion historica 
		
		try:
			objetivo_his=objetivo_intervencionhistoria.objects.filter(Estudiante__id=pk)
			objetivo_his.delete()
		except objetivo_intervencionhistoria.DoesNotExist:
			obje=None	

		try:
			evaluacion=Diagnostico.objects.get(Estudiante__id=pk)
			Diagnostico_historia.objects.create(Historia=history,fecha=evaluacion.fecha,
			situacion_actual=evaluacion.situacion_actual,observaciones=evaluacion.observaciones,
			familia=evaluacion.familia,usuario=evaluacion.usuario)
			evaluacion.delete()	

		#Borrar los objetivos de intervencion historica 
		except Diagnostico.DoesNotExist:
			evaluacion=None
			#Diagnostico_historia.objects.create(Historia=history,fecha=datetime.date.today(),
			#situacion_actual='sin registro',observacion='sin observación',familia='sin sugerencias',usuario=None)

		try:
			salir=Ficha_de_egreso.objects.get(Estudiante__id=pk)
			Ficha_de_egreso_historia.objects.create(Historia=history,fecha_informe=salir.fecha,
			fecha_egreso=salir.fecha_egreso,Motivo_egreso=salir.Motivo_egreso,sintesis=salir.sintesis,
			sugerencias=salir.sugerencias,usuario=salir.usuario)
			salir.delete()
	

		#Borrar los objetivos de intervencion historica 
		except Ficha_de_egreso.DoesNotExist:
			salir=None

		try:
			continuidad=Reporte_continuidad.objects.filter(Estudiante__id=pk)
			for continuo in continuidad.all():
				Reporte_continuidad_historia.objects.create(Historia=history,fecha=continuo.fecha,
					motivo=continuo.motivo,antecedentes=continuo.antecedentes,observaciones=continuo.observaciones,
					sugerencias=continuo.sugerencias,usuario=continuo.usuario)
				continuo.delete()	
		except Reporte_continuidad.DoesNotExist:
			continuidad=None
	
		ficha.estado=2
		ficha.save()
		#Borrra retorno a una institucion y lo graba en historia
		intervenido.delete()
		agendo.delete()
		

		return redirect('derivacion:intervencion_listar')
	
		
	return render(request,"historia/aviso_termino_dupla.html",context)




# ---------------------

	
class registro_historico(ListView):
	model=Historia
	paginate_by = 6
	template_name = 'historia/registro_historico.html'
	

	def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
		context = super(registro_historico, self).get_context_data(**kwargs)
	
		return context	

def ver_historia_objetivos(request,pk,estudiante):
	
	
	objetivos=objetivo_intervencion_historico.objects.get(Historia__id=pk)
	dato=Estudiante.objects.get(pk=estudiante)
	history=Historia.objects.get(pk=pk)
	tematicas=history.objetivo_intervencion
	template = 'historia/ver_historia_objetivos.html'
	context = {
        "objetivos":objetivos,
        "dato":dato,
        "tematicas":tematicas,
       
    }
	return render(request, template, context)
	

def ver_historia_ficha_derivacion(request,pk,estudiante):
	
	
	try:
		history=Historia.objects.get(pk=pk)
		ficha=history.Ficha_derivacion
	except Historia.DoesNotExist:
		history=None
		
	
	dato=Estudiante.objects.get(pk=estudiante)
	
	

	template = 'historia/ver_historia_ficha_derivacion.html'
	context = {
       
        "ficha":ficha,
        "estudiante":dato,
        "historia":history,
    }
	return render(request, template, context)





def ver_historia_sesiones(request,pk,estudiante):
	
	history=Historia.objects.get(pk=pk)
	try:
		objetivos=objetivo_intervencion_historico.objects.get(Historia__id=pk)
	except objetivo_intervencion_historico.DoesNotExist:
		objetivos=""

	try:
		retorno=Motivo_Retorno_historia.objects.get(Historia__id=pk)
	except Motivo_Retorno_historia.DoesNotExist:
		retorno=""
			
	try:
		sesion=agenda_historica.objects.filter(Historia=pk)
	except agenda_historica.DoesNotExist:
		sesion=""
	try:
		fin=agenda_historica.objects.filter(Historia=history)
		
		ultimo=fin.order_by('fecha').latest('numero')
		
		total=fin.filter(Historia=history).count()
	except agenda_historica.DoesNotExist:
		ultimo=None	
		total=None
	
	dato=Estudiante.objects.get(pk=estudiante)
	template = 'historia/ver_historia_sesiones.html'
	context = {
        "objetivos":objetivos,
        "sesiones":sesion,
        "dato":dato,
        "retorno":retorno,
        "Historia":history,
        "ultimo":ultimo,
        "total":total,
       
    }
	return render(request, template, context)

def evaluacion_historia(request,pk,historia):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	history=Historia.objects.get(pk=historia)
	ficha=history.Ficha_derivacion
	
	try:
		evaluado=Diagnostico_historia.objects.get(Historia=history)
		form = DiagnosticoForm(instance=evaluado or None)
	except Diagnostico_historia.DoesNotExist:
		evaluado=None
		form = DiagnosticoForm(None)
	
	mensaje="Informe de evaluación Historico"        	
	return render(
        request,
        'historia/reporte_caso.html',
        context={'formulario':form,
        		'estudiante':estudiante_id,
        		 'historia':history,
        		 'ficha':ficha,
        		 'mensaje':mensaje,
        		 
	})	
def final_historia(request,pk,historia):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	history=Historia.objects.get(pk=historia)
	ficha=history.Ficha_derivacion
	try:
		evaluado=Ficha_de_egreso_historia.objects.get(Historia=history)
		form = FichaEgresoForm(instance=evaluado or None)
	except Ficha_de_egreso_historia.DoesNotExist:
		evaluado=None
		form = FichaEgresoForm(None)
	
	mensaje="Informe de egreso historia"        	
	return render(
        request,
        'historia/ficha_egreso.html',
        context={'formulario':form,
        		'estudiante':estudiante_id,
        		 'historia':history,
        		 'ficha':ficha,
        		 'mensaje':mensaje,
        	

	})	


def VerReportecontinuidad_historia(request,pk,historia):
    
	estudiante_id=Estudiante.objects.get(pk=pk)
	history=Historia.objects.get(Estudiante__id=pk)

	try:
		
		informes=Reporte_continuidad_historia.objects.filter(Historia=history)
	except Reporte_continuidad_historia.DoesNotExist:
		informes=None
	
    
	return render(
        request,
        'historia/listado_continuidad.html',
        context={'informes':informes,
        		'dato':estudiante_id,
        		'historia':historia
        	        		 

	})	

def ReportecontinuidadModificar_historia(request,pk,continuidad,historia):
	mensaje=""
	
	dato=Estudiante.objects.get(pk=pk)
	fase2=Reporte_continuidad_historia.objects.get(pk=continuidad)
	history=Historia.objects.get(pk=historia)
	obje=history.objetivo_intervencion

		
	if request.method == 'POST':
		form = ContinuidadForm(request.POST or None)
			
		return redirect('historia:registro_historico')
	        
		
	print continuidad
	print historia
	form = ContinuidadForm( instance=fase2)
	return render(
			        request,
			        'historia/reporte_continuidad.html',
			        context={'formulario':form,
		        	'dato':dato,
		       		'objetivo':obje,
	        		'mensaje':mensaje,
	        		'continuidad':fase2,


	            		 
		})
# Vista sobre la estadistica de la aplicación tematicas 

class EstudiantevsTematicas(ListView):
	
	template_name = 'historia/estudiantevstematicas.html'
	def get_queryset(self, *args, **kwargs):
		return objetivo_intervencion.objects.filter(activo=1)
#Tematicas por cantidad 
class EstudiantevsTematicasCantidadActual(ListView):
	
	template_name = 'historia/estudiantevstematicas.html'
	def get_queryset(self, *args, **kwargs):
		
		return objetivo_intervencion.objects.filter(activo=1)	

class Listadointervenidos(ListView):
	
	template_name = 'historia/estudiantevsintervencion.html'
	def get_queryset(self, *args, **kwargs):
		

		return Ficha_derivacion.objects.filter(estado=1)

	def get_context_data(self, **kwargs):
		context = super(Listadointervenidos, self).get_context_data(**kwargs)
		estudiantesahistoricos = Ficha_derivacion.objects.filter(estado=2)
		context['historicos'] = estudiantesahistoricos

