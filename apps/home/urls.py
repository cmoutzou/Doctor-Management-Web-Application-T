# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import *



urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('export_csv',views.export_csv,name='export_csv'),
	path('insert_patient',views.insert_patient,name='insert_patient'), 
    path('insert_patient_L',views.insert_patient_L,name='insert_patient_L'),
    path('insert_patient2',views.insert_patient2,name='insert_patient2'),
	path('nurse_patient.html',views.nurse_patient,name='nurse_patient'),
    path('exam_table.html',views.exam_table,name='exam_table'),
    path('exam_table_L.html',views.exam_table_L,name='exam_table_L'),  
    path('exam_patient/<int:prk>',views.exam_patient,name='exam_patient'),
    path('exam_patient.html',views.exam_patient,name='exam_patient'),
    path('load_pdf_exam_patient',views.load_pdf_exam_patient,name='load_pdf_exam_patient'),
    path('exam_patient_L.html',views.exam_patient_L,name='exam_patient_L'),
    path('exam_patient_L/<int:prk>',views.exam_patient_L,name='exam_patient_L'),
    path('cost_patient',views.cost_patient,name='cost_patient'),
    path('profile/<int:prk>', views.profile, name='profile'),
    path('update_profile/<int:prk>', views.update_profile, name='update_profile'),
    path('update_patient_form',views.update_patient_form,name='update_patient_form'),
    path('update_profile_L/<int:prk>', views.update_profile_L, name='update_profile_L'),
    path('update_patient_form_L',views.update_patient_form_L,name='update_patient_form_L'),
    path('profile_L/<int:prk>', views.profile_L, name='profile_L'),
    path('invoice.html', views.invoice, name='invoice'),
    path('invoice_analysis/<str:period>/', views.invoice_analysis, name='invoice_analysis'),
    path('invoice_L.html', views.invoice_L, name='invoice_L'),
    path('invoice_L_analysis/<str:period>/', views.invoice_L_analysis, name='invoice_L_analysis'),
    path('agenta.html', views.agenta, name='agenta'),
    path('add_event', views.add_event, name='add_event'),
    path('new_event', views.new_event, name='new_event'),
    path('update_event', views.update_event, name='update_event'),
    path('update_event_form', views.update_event_form, name='update_event_form'),
    path('some_view/<int:prk>', views.some_view, name='some_view'),
   
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
	

]

