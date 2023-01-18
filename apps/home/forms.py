from django import forms
from .models import PatientExam,PatientHosp,Exams,Insurance,lifecheck,Events
from django.forms import ModelForm



class forminsert_patient(forms.ModelForm):
	class Meta:
		model=PatientExam
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]



class forminsert_nurse(forms.ModelForm):
	class Meta:
		model=PatientHosp
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]

class forminsert_patient_L(forms.ModelForm):
	class Meta:
		model=lifecheck
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]		

class formupdate_patient(forms.ModelForm):
	class Meta:
		model=PatientExam
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]

class formupdate_patient_L(forms.ModelForm):
	class Meta:
		model=lifecheck
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]		


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=550)
    file = forms.FileField()		

class add_event(forms.ModelForm):
	class Meta:
		model=Events
		fields = '__all__'#['name','age','asfaleia','energeia','date_exam','istoriko','gnomateusi','odigies','cost','amka',]

	