/*
	autor: @drincastX
	descripcion: Funcion dummy para crear un objeto JSON, retorna una lista de objetos JSON
*/
function obtenerObjJson(){
	var obj = [{"Fecha":"10/07/2017", "Horario":"10:30 -11:00", "Tipo Actividad":"Sesion 1","Observaciones ":""},
			{"Fecha":"17/07/2017", "Horario":"13:30 -14:30", "Tipo Actividad":"Sesion 2","Observaciones ":""},
			{"Fecha":"24/07/2017", "Horario":"11:30 -12:30", "Tipo Actividad":"Sesion 3","Observaciones ":""},
			{"Fecha":"31/07/2017", "Horario":"10:30 -11:00", "Tipo Actividad":"No asiste avisa","Observaciones ":"Re agenda para 01/08/2017"},
			{"Fecha":"1/08/2017", "Horario":"10:30 -11:00", "Tipo Actividad":"Sesion 4","Observaciones ":"si"},
			{"Establecimiento":" Establecimiento:La Araucaria ", "Curso":"Curso :3 año A", "Fecha de ingreso":"Fecha de ingreso : 10/07/2017","Fecha de derivacion ":"Fecha de derivacion : 01/07/2017"}

			  ];
	return obj;
}

/*
	autor: @drincastX
	descripcion: Funcion que crea una tabla dinamica en base a un objeto JSON, aun elemento div y a un nombre de clase de estilo css
*/
function crearTablaSimple(divTabla, classDivTabla, objJson){
	var contenedorTabla;
	var fTemp;
	var i, j;
	var arrayClaves = new Array();
	var classFilaDatos = "TBLFilaDatosPar"; //indica fila impar

	
	try{
		
		contenedorTabla = document.getElementById(divTabla);
		contenedorTabla.className = classDivTabla;
		fTemp = objJson[0];
	
		var tabla = document.createElement("table");	//la tabla
		tabla.id = divTabla + "TBL";					//le asignamos un id dinamico a la tabla
		var fila = document.createElement("tr");		//la primera fila de la tabla y corresponde a la cabecera
		fila.id = divTabla + "TBLCabecera";				//se le asigna un id dinamico a la fila de la cabecera
		fila.className = "TBLCabecera";					//le asignamos el nombre de clase de estilo fijo a la fila de la cabecera
		var celda;

		//ciclo para sacar los key (claves) del objeto JSON y agregar las celdas a la fila de cabecera
		for(i in fTemp){
			arrayClaves.push(i);
			celda = document.createElement("th");
			celda.innerHTML = i;
			fila.appendChild(celda);
		}
		tabla.appendChild(fila);
		contenedorTabla.appendChild(tabla);

		i=0;
		//ciclo para crear las filas de datos
		for(i; i < objJson.length; i++){
			fTemp = objJson[i];
			fila = document.createElement("tr");
			fila.id = divTabla + "tblDatos" + i;
			fila.className = classFilaDatos;

			if(classFilaDatos === 'TBLFilaDatosPar'){
				classFilaDatos = 'TBLFilaDatosImpar';
			}else{
				classFilaDatos = 'TBLFilaDatosPar';
			}

			//subciclo para crear las celdas y agregarla a la fila correspondiente
			for(j in fTemp){
				celda = document.createElement("td");
				celda.innerHTML = fTemp[j];
				fila.appendChild(celda);
			}
			tabla.appendChild(fila);
		}
	}
	catch(err){
		alert("Error al procesar la tabla de datos");
		console.log(err);
	}
	finally{}
}

/*
	Esta obra está sujeta a la licencia Reconocimiento-CompartirIgual 4.0 Internacional de Creative Commons. Para ver una copia de esta licencia, visite http://creativecommons.org/licenses/by-sa/4.0/.
*/