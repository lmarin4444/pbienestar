from django import forms
from secretaria.models import MascotaRA,agenda
from informe.models import formatos


class UploadForm(forms.ModelForm):

	class Meta:
		model = formatos

		fields = [

			
			'nombre',
			'docfile1',

		]
		labels = {

			
			'nombre': 'Nombre',
			'docfile1': 'Archivo',
		}
		widgets = {


			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'docfile1':forms.FileInput(attrs={'class':'form-control'}),
		}



 	






