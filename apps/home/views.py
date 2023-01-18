# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request, HttpResponseBadRequest, JsonResponse
from django.template import loader, Template, Context
from django.urls import reverse
from .models import PatientExam, PatientHosp, Exams, Exam_cost, Insurance, lifecheck,Events
from django.shortcuts import render, redirect
from django.db import connection, models
from .forms import forminsert_patient, forminsert_nurse, forminsert_patient_L, UploadFileForm, formupdate_patient, formupdate_patient_L,add_event
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django_tables2 import RequestConfig
import datetime
import PyPDF2
import re
import json
import js
from mirage.crypto import Crypto
import csv
import unicodecsv as csv
import requests
import bs4
import xlwt
from datetime import date
from django.contrib.auth.models import User
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas



@login_required(login_url="/login/")
def index(request):
    patient = PatientExam.objects.all().order_by('-date_exam')[:5]
    events=Events.objects.all().filter(start_date__gte=datetime.datetime.strptime(str(date.today()),'%Y-%m-%d'),start_date__lte=datetime.datetime.strptime(str(date.today()),'%Y-%m-%d')).order_by('start_date')[:3]
    cursor = connection.cursor()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where date_exam=curdate()')
    daily_revenue = cursor.fetchone()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where month(date_exam)=month(curdate())')
    monthly_revenue = cursor.fetchone()
    cursor.execute('select count(*) from patient_exam')
    total_visits_biokliniki = cursor.fetchone()
    cursor.execute('select count(*) from lifecheck')
    total_visits_lifecheck = cursor.fetchone()
    cursor.execute('select round(sum(cost),2) from patient_exam')
    total_revenue = cursor.fetchone()
    res = requests.get("https://www.hts.org.gr/news")
    soup = bs4.BeautifulSoup(res.text,"lxml")
    news_dates = soup.select('.date')
    news_text=soup.select('.subject')
    news_links=soup.select('.subject > a')
    news=[]
    for i in range(len(news_dates)-1):
        news.append({'date':'','text':'','link':''})
        news[i]['date']=news_dates[i].getText()
        news[i]['text']=news_text[i].getText()
        news[i]['link']=re.search('href="(.*)">', str(news_links[i])).group(1)
    context = {'news':news,
                'patient': patient,
               'daily_revenue': daily_revenue,
               'monthly_revenue': monthly_revenue,
               'total_revenue': total_revenue,
               'total_visits_biokliniki': total_visits_biokliniki,
               'total_visits_lifecheck': total_visits_lifecheck,
               'events': events,}
    html_template = loader.get_template('home\index.html')
    return HttpResponse(html_template.render(context, request))



def profile(request, prk):
    patient = PatientExam.objects.get(prk=prk)
    cursor = connection.cursor()
    files=PatientExam.objects.filter(amka=patient.amka)
    nfiles = PatientExam.objects.raw(
        f'SELECT prk,EXAM_FILE file1,date_exam,istoriko,gnomateusi,FVC_PRED,FVC_BEST,FVC_POST,FVC_POST_PRED,FEV1_PRED,FEV1_BEST,FEV1_POST,FEV1_POST_PRED,FEV1_FVC_PRED,FEV1_FVC_BEST,FEV1_FVC_POST,FEV1_FVC_POST_PRED FROM PATIENT_EXAM P WHERE amka={patient.amka} order by date_exam')
    fdata = {}
    num_file = 0
    first_file = ['']
    data = []
    i = 0
    for file in files:
        if file.exam_file is not None:
            fdata[i] = {}
            fdata[i]['exam_date'] = file.date_exam
            fdata[i]['FVC_Pred'] = file.FVC_PRED
            fdata[i]['FVC_Best'] = file.FVC_BEST
            if(file.FVC_POST!=''):
                fdata[i]['FVC_Post'] = file.FVC_POST
            else:
                fdata[i]['FVC_Post'] = 0
            if(file.FVC_POST_PRED!=''):
                fdata[i]['FVC_Post_Pred'] = file.FVC_POST_PRED
            else:
                fdata[i]['FVC_Post_Pred']=0
            fdata[i]['FEV1_Pred'] = file.FEV1_PRED
            fdata[i]['FEV1_Best'] = file.FEV1_BEST
            if(file.FEV1_POST!=''):
                fdata[i]['FEV1_Post'] = file.FEV1_POST
            else:
                fdata[i]['FEV1_Post'] = 0
            if(file.FEV1_POST_PRED!=''):
                fdata[i]['FEV1_Post_Pred'] = file.FEV1_POST_PRED
            else:
                fdata[i]['FEV1_Post_Pred']=0
            fdata[i]['FEV1/FVC_Pred'] = file.FEV1_FVC_PRED
            fdata[i]['FEV1/FVC_Best'] = file.FEV1_FVC_BEST
            if(file.FEV1_FVC_POST!=''):
                fdata[i]['FEV1/FVC_Post'] = file.FEV1_FVC_POST
            else:
                fdata[i]['FEV1/FVC_Post'] = 0
            if(file.FEV1_POST_PRED!=''):
                fdata[i]['FEV1/FVC_Post_Pred'] = file.FEV1_FVC_POST_PRED
            else:
                fdata[i]['FEV1/FVC_Post_Pred']=0       

            i += 1
            chart = {'y': file.date_exam,
                    'a': fdata[i-1]['FVC_Pred'],
                    'b': fdata[i-1]['FVC_Best'],
                    'c': fdata[i-1]['FVC_Post'],
                    'd': fdata[i-1]['FVC_Post_Pred'],
                    'e': fdata[i-1]['FEV1_Pred'],
                    'f': fdata[i-1]['FEV1_Best'],
                    'g': fdata[i-1]['FEV1_Post'],
                    'h': fdata[i-1]['FEV1_Post_Pred'],
                    'i': fdata[i-1]['FEV1/FVC_Pred'],
                    'j': fdata[i-1]['FEV1/FVC_Best'],
                    'k': fdata[i-1]['FEV1/FVC_Post'],
                    'l': fdata[i-1]['FEV1/FVC_Post_Pred']}
            data.append(chart)
    patient_data = PatientExam.objects.all().filter(
            amka=patient.amka).order_by('date_exam')

    context = {'files': nfiles,
                'patient': patient,
                'patient_data': patient_data,
                'fdata': fdata}

    context['chart_data'] = json.dumps({
        'titles': 'FVC',
        'element': 'morris-bar-chart',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': ['a', 'b', 'c',' d'],  # it can be custom
        'labels': ['FVC_Pred', 'FVC_Best', 'FVC_Post','FVC_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data2'] = json.dumps({
        'element': 'morris-bar-chart2',
        'titles': 'FEV1',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': [ 'e', 'f', 'g', 'h'],  # it can be custom
        'labels': ['FEV1_Pred', 'FEV1_Best', 'FEV1_Post','FEV1_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data3'] = json.dumps({
        'element': 'morris-bar-chart3',
        'titles': 'FEV1/FVC',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': [ 'i', 'j', 'k', 'l'],  # it can be custom
        'labels': ['FEV1/FVC_Pred', 'FEV1/FVC_Best', 'FEV1/FVC_Post','FEV1/FVC_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    html_template = loader.get_template('home\profile.html')
    return HttpResponse(html_template.render(context, request))


def profile_L(request, prk):
    patient = lifecheck.objects.get(prk=prk)
    cursor = connection.cursor()
    files=lifecheck.objects.filter(amka=patient.amka)
    #files = PatientExam.objects.raw(
        #f'SELECT prk,EXAM_FILE file1,date_exam,istoriko,gnomateusi,FVC_PRED,FVC_BEST,FVC_POST,FVC_POST_PRED,FEV1_PRED,FEV1_BEST,FEV1_POST,FEV1_POST_PRED,FEV1_FVC_PRED,FEV1_FVC_BEST,FEV1_FVC_POST,FEV1_FVC_POST_PRED FROM PATIENT_EXAM P WHERE amka={patient.amka} order by date_exam')
    fdata = {}
    num_file = 0
    first_file = ['']
    data = []
    i = 0
    for file in files:
        if file.exam_file is not None:
            fdata[i] = {}
            fdata[i]['exam_date'] = file.date_exam
            fdata[i]['FVC_Pred'] = file.FVC_PRED
            fdata[i]['FVC_Best'] = file.FVC_BEST
            if(file.FVC_POST!=''):
                fdata[i]['FVC_Post'] = file.FVC_POST
            else:
                fdata[i]['FVC_Post'] = 0
            if(file.FVC_POST_PRED!=''):
                fdata[i]['FVC_Post_Pred'] = file.FVC_POST_PRED
            else:
                fdata[i]['FVC_Post_Pred']=0
            fdata[i]['FEV1_Pred'] = file.FEV1_PRED
            fdata[i]['FEV1_Best'] = file.FEV1_BEST
            if(file.FEV1_POST!=''):
                fdata[i]['FEV1_Post'] = file.FEV1_POST
            else:
                fdata[i]['FEV1_Post'] = 0
            if(file.FEV1_POST_PRED!=''):
                fdata[i]['FEV1_Post_Pred'] = file.FEV1_POST_PRED
            else:
                fdata[i]['FEV1_Post_Pred']=0
            fdata[i]['FEV1/FVC_Pred'] = file.FEV1_FVC_PRED
            fdata[i]['FEV1/FVC_Best'] = file.FEV1_FVC_BEST
            if(file.FEV1_FVC_POST!=''):
                fdata[i]['FEV1/FVC_Post'] = file.FEV1_FVC_POST
            else:
                fdata[i]['FEV1/FVC_Post'] = 0
            if(file.FEV1_POST_PRED!=''):
                fdata[i]['FEV1/FVC_Post_Pred'] = file.FEV1_FVC_POST_PRED
            else:
                fdata[i]['FEV1/FVC_Post_Pred']=0       

            i += 1
            chart = {'y': file.date_exam,
                    'a': fdata[i-1]['FVC_Pred'],
                    'b': fdata[i-1]['FVC_Best'],
                    'c': fdata[i-1]['FVC_Post'],
                    'd': fdata[i-1]['FVC_Post_Pred'],
                    'e': fdata[i-1]['FEV1_Pred'],
                    'f': fdata[i-1]['FEV1_Best'],
                    'g': fdata[i-1]['FEV1_Post'],
                    'h': fdata[i-1]['FEV1_Post_Pred'],
                    'i': fdata[i-1]['FEV1/FVC_Pred'],
                    'j': fdata[i-1]['FEV1/FVC_Best'],
                    'k': fdata[i-1]['FEV1/FVC_Post'],
                    'l': fdata[i-1]['FEV1/FVC_Post_Pred']}
            data.append(chart)
    patient_data = lifecheck.objects.all().filter(
            amka=patient.amka).order_by('date_exam')

    context = {'files': files,
                'patient': patient,
                'patient_data': patient_data,
                'fdata': fdata}

    context['chart_data'] = json.dumps({
        'titles': 'FVC',
        'element': 'morris-bar-chart',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': ['a', 'b', 'c',' d'],  # it can be custom
        'labels': ['FVC_Pred', 'FVC_Best', 'FVC_Post','FVC_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data2'] = json.dumps({
        'element': 'morris-bar-chart2',
        'titles': 'FEV1',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': [ 'e', 'f', 'g', 'h'],  # it can be custom
        'labels': ['FEV1_Pred', 'FEV1_Best', 'FEV1_Post','FEV1_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data3'] = json.dumps({
        'element': 'morris-bar-chart3',
        'titles': 'FEV1/FVC',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': [ 'i', 'j', 'k', 'l'],  # it can be custom
        'labels': ['FEV1/FVC_Pred', 'FEV1/FVC_Best', 'FEV1/FVC_Post','FEV1/FVC_Post_Pred'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    html_template = loader.get_template('home\profile_L.html')
    return HttpResponse(html_template.render(context, request))
    


def update_profile(request, prk):
    # prk=request.GET.get('prk')
    patient = PatientExam.objects.get(prk=prk)
    cursor = connection.cursor()
    #cursor.execute(f'SELECT p.*,SUBSTR(EXAM_FILE,20) exam_file FROM PATIENT_EXAM P WHERE amka={patient.amka}')
    files = PatientExam.objects.raw(
        f'SELECT prk,EXAM_FILE file1,date_exam,istoriko,gnomateusi,FVC_PRED,FVC_BEST,FVC_POST,FVC_POST_PRED,FEV1_PRED,FEV1_BEST,FEV1_POST,FEV1_POST_PRED,FEV1_FVC_PRED,FEV1_FVC_BEST,FEV1_FVC_POST,FEV1_FVC_POST_PRED FROM PATIENT_EXAM P WHERE prk={patient.prk} order by date_exam')
    #cursor.execute(f'SELECT * FROM PATIENT_EXAM  WHERE amka=(select amka from patient_exam where PRK={prk})')
    #patient_data = cursor.fetchone()
    patient_data = PatientExam.objects.all().filter(
        prk=patient.prk).order_by('date_exam')
    context = {'files': files,
               'patient': patient,
               'patient_data': patient_data}
    html_template = loader.get_template('home\\update_profile.html')
    return HttpResponse(html_template.render(context, request))
    


def update_patient_form(request):
    form = formupdate_patient(request.POST, request.FILES)
    if form.is_valid():
        prk = request.POST.get('prk')
        patient = PatientExam.objects.get(prk=prk)
        cursor = connection.cursor()
        files = PatientExam.objects.raw(
            f'SELECT prk,SUBSTR(EXAM_FILE,20) file1,date_exam,istoriko,gnomateusi FROM PATIENT_EXAM P WHERE prk={patient.prk} order by date_exam')
        for file in files:
            patient = PatientExam.objects.get(prk=prk)
            patient.name = request.POST.get('name') 
            patient.surname = request.POST.get('surname')
            patient.date_birth = request.POST.get('date_birth')
            patient.amka = request.POST.get('amka')
            patient.FVC_PRED = request.POST.get('FVC_PRED')
            patient.FVC_BEST = request.POST.get('FVC_BEST')
            patient.FVC_POST = request.POST.get('FVC_POST')
            patient.FVC_POST_PRED = request.POST.get('FVC_POST_PRED')
            patient.FEV1_PRED = request.POST.get('FEV1_PRED')
            patient.FEV1_BEST = request.POST.get('FEV1_BEST')
            patient.FEV1_POST = request.POST.get('FEV1_POST')
            patient.FEV1_POST_PRED = request.POST.get('FEV1_POST_PRED')
            patient.FEV1_FVC_PRED = request.POST.get('FEV1_FVC_PRED')
            patient.FEV1_FVC_BEST = request.POST.get('FEV1_FVC_BEST')
            patient.FEV1_FVC_POST = request.POST.get('FEV1_FVC_POST')
            patient.FEV1_FVC_POST_PRED = request.POST.get('FEV1_FVC_POST_PRED')
            #patient.exam_file = request.FILES['exam_file']
            patient.istoriko = request.POST.get('history' + str(patient.prk))
            patient.cat = request.POST.get('cat' + str(patient.prk))
            patient.cardio = request.POST.get('cardio' + str(patient.prk))
            patient.energeia = request.POST.get('energeia' + str(patient.prk))
            patient.current_disease = request.POST.get('current_disease' + str(patient.prk))
            patient.family_history = request.POST.get('family_history' + str(patient.prk))
            patient.allergies = request.POST.get('allergies' + str(patient.prk))
            patient.vaccine = request.POST.get('vaccine' + str(patient.prk))
            patient.baseline = request.POST.get('baseline' + str(patient.prk))
            patient.ergastiriaka = request.POST.get('ergastiriaka' + str(patient.prk))
            patient.tep = request.POST.get('tep' + str(patient.prk))
            patient.katoikon = request.POST.get('katoikon' + str(patient.prk))
            patient.conclusion = request.POST.get('conclusion' + str(patient.prk))
            patient.suggestion = request.POST.get('suggestion' + str(patient.prk))
            patient.followup = request.POST.get('followup' + str(patient.prk))
            patient.proliptikos = request.POST.get('proliptikos' + str(patient.prk))
            # you can update other fields by using object.field_name (e.g. profile_pic.text = request.POST.get['text']
            #update_patient = PatientExam.objects.raw(f'UPDATE PATIENT_EXAM SET NAME='{patient.name}',SURNAME='{patient.surname}',DATE_BIRTH='{patient.date_birth}',AMKA='{patient.amka}',ISTORIKO='{patient.istoriko}',FVC_PRED='{patient.FVC_PRED}',FVC_BEST='{patient.FVC_BEST}',FVC_POST='{patient.FVC_POST}',FVC_POST_PRED='{patient.FVC_POST_PRED}',FEV1_PRED='{patient.FEV1_PRED}',FEV1_BEST='{patient.FEV1_BEST}',FEV1_POST='{patient.FEV1_POST}',FEV1_POST_PRED='{patient.FEV1_POST_PRED}',FEV1_FVC_PRED='{patient.FEV1_FVC_PRED}',FEV1_FVC_BEST='{patient.FEV1_FVC_BEST}',FEV1_FVC_POST='{patient.FEV1_FVC_POST}',FEV1_FVC_POST_PRED='{patient.FEV1_FVC_POST_PRED}',EXAM_FILE=(SELECT EXAM_FILE FROM (SELECT EXAM_FILE FROM PATIENT_EXAM WHERE PRK=(SELECT MAX(E.PRK) FROM PATIENT_EXAM E)) AS A) WHERE prk='{file.prk}'")
        form.save()
        with connection.cursor() as cursor:
            exam_file = cursor.execute(
                "SELECT EXAM_FILE FROM PATIENT_EXAM WHERE PRK=(SELECT MAX(PRK) FROM PATIENT_EXAM)")
            row = cursor.fetchone()
        with connection.cursor() as cursor:
            #cursor.execute(f"UPDATE PATIENT_EXAM SET NAME='{patient.name}',SURNAME='{patient.surname}',DATE_BIRTH='{patient.date_birth}',AMKA='{patient.amka}',ISTORIKO='{patient.istoriko}',EXAM_FILE=CONCAT(EXAM_FILE,',',(SELECT EXAM_FILE FROM (SELECT EXAM_FILE FROM PATIENT_EXAM WHERE PRK=(SELECT MAX(E.PRK) FROM PATIENT_EXAM E)) AS A)) WHERE prk='{patient.prk}'")
            cursor.execute(
                f"UPDATE PATIENT_EXAM SET NAME='{patient.name}',SURNAME='{patient.surname}',DATE_BIRTH='{patient.date_birth}',AMKA='{patient.amka}',ISTORIKO='{patient.istoriko}',cardio='{patient.cardio}',energeia='{patient.energeia}',current_disease='{patient.current_disease}',family_history='{patient.family_history}',allergies='{patient.allergies}',vaccine='{patient.vaccine}',baseline='{patient.baseline}',ergastiriaka='{patient.ergastiriaka}',tep='{patient.tep}',katoikon='{patient.katoikon}',conclusion='{patient.conclusion}',suggestion='{patient.suggestion}',followup='{patient.followup}',proliptikos='{patient.proliptikos}',FVC_PRED='{patient.FVC_PRED}',FVC_BEST='{patient.FVC_BEST}',FVC_POST='{patient.FVC_POST}',FVC_POST_PRED='{patient.FVC_POST_PRED}',FEV1_PRED='{patient.FEV1_PRED}',FEV1_BEST='{patient.FEV1_BEST}',FEV1_POST='{patient.FEV1_POST}',FEV1_POST_PRED='{patient.FEV1_POST_PRED}',FEV1_FVC_PRED='{patient.FEV1_FVC_PRED}',FEV1_FVC_BEST='{patient.FEV1_FVC_BEST}',FEV1_FVC_POST='{patient.FEV1_FVC_POST}',FEV1_FVC_POST_PRED='{patient.FEV1_FVC_POST_PRED}',EXAM_FILE=(SELECT EXAM_FILE FROM (SELECT EXAM_FILE FROM PATIENT_EXAM WHERE PRK=(SELECT MAX(E.PRK) FROM PATIENT_EXAM E)) AS A) WHERE prk='{prk}'")
            row = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM PATIENT_EXAM WHERE  ASFALEIA IS NULL AND ENERGEIA IS NULL")
            row = cursor.fetchone()
            messages.success(request, "Ο Ασθενής καταχωρήθηκε επιτυχώς!")
    return redirect(request.META['HTTP_REFERER'])


def update_profile_L(request, prk):
    # prk=request.GET.get('prk')
    patient = lifecheck.objects.get(prk=prk)
    cursor = connection.cursor()
    #cursor.execute(f'SELECT p.*,SUBSTR(EXAM_FILE,20) exam_file FROM PATIENT_EXAM P WHERE amka={patient.amka}')
    files = lifecheck.objects.raw(
        f'SELECT prk,SUBSTR(EXAM_FILE,20) file1,date_exam,istoriko,gnomateusi FROM lifecheck P WHERE amka={patient.amka} order by date_exam')
    #cursor.execute(f'SELECT * FROM PATIENT_EXAM  WHERE amka=(select amka from patient_exam where PRK={prk})')
    #patient_data = cursor.fetchone()
    patient_data = lifecheck.objects.all().filter(
        amka=patient.amka).order_by('date_exam')
    context = {'files': files,
               'patient': patient,
               'patient_data': patient_data}
    html_template = loader.get_template('home\\update_profile_L.html')
    return HttpResponse(html_template.render(context, request))


def update_patient_form_L(request):
    form = formupdate_patient_L(request.POST, request.FILES)
    if form.is_valid():
        prk = request.POST.get('prk')
        patient = lifecheck.objects.get(prk=prk)
        cursor = connection.cursor()
        files = lifecheck.objects.raw(
            f'SELECT prk,SUBSTR(EXAM_FILE,20) file1,date_exam,istoriko,gnomateusi FROM LIFECHECK P WHERE amka={patient.amka} order by date_exam')
        for file in files:
            patient = lifecheck.objects.get(prk=file.prk)
            patient.name = request.POST.get('name')
            patient.surname = request.POST.get('surname')
            patient.date_birth = request.POST.get('date_birth')
            patient.amka = request.POST.get('amka')
            patient.FVC_PRED = request.POST.get('FVC_PRED')
            patient.FVC_BEST = request.POST.get('FVC_BEST')
            patient.FVC_POST = request.POST.get('FVC_POST')
            patient.FVC_POST_PRED = request.POST.get('FVC_POST_PRED')
            patient.FEV1_PRED = request.POST.get('FEV1_PRED')
            patient.FEV1_BEST = request.POST.get('FEV1_BEST')
            patient.FEV1_POST = request.POST.get('FEV1_POST')
            patient.FEV1_POST_PRED = request.POST.get('FEV1_POST_PRED')
            patient.FEV1_FVC_PRED = request.POST.get('FEV1_FVC_PRED')
            patient.FEV1_FVC_BEST = request.POST.get('FEV1_FVC_BEST')
            patient.FEV1_FVC_POST = request.POST.get('FEV1_FVC_POST')
            patient.FEV1_FVC_POST_PRED = request.POST.get('FEV1_FVC_POST_PRED')
            patient.istoriko = request.POST.get('history' + str(patient.prk))
            # you can update other fields by using object.field_name (e.g. profile_pic.text = request.POST.get['text']
            #update_patient = PatientExam.objects.raw(f'UPDATE LIFECHECK SET NAME={patient.name},SURNAME={patient.surname},DATE_BIRTH={patient.date_birth},AMKA={patient.amka},history={patient.history} WHERE prk={patient.prk}')
        form.save()
        with connection.cursor() as cursor:
            exam_file = cursor.execute(
                "SELECT EXAM_FILE FROM LIFECHECK WHERE PRK=(SELECT MAX(PRK) FROM LIFECHECK)")
            row = cursor.fetchone()
        with connection.cursor() as cursor:
            f"UPDATE PATIENT_EXAM SET NAME='{patient.name}',SURNAME='{patient.surname}',DATE_BIRTH='{patient.date_birth}',AMKA='{patient.amka}',ISTORIKO='{patient.istoriko}',FVC_PRED='{patient.FVC_PRED}',FVC_BEST='{patient.FVC_BEST}',FVC_POST='{patient.FVC_POST}',FVC_POST_PRED='{patient.FVC_POST_PRED}',FEV1_PRED='{patient.FEV1_PRED}',FEV1_BEST='{patient.FEV1_BEST}',FEV1_POST='{patient.FEV1_POST}',FEV1_POST_PRED='{patient.FEV1_POST_PRED}',FEV1_FVC_PRED='{patient.FEV1_FVC_PRED}',FEV1_FVC_BEST='{patient.FEV1_FVC_BEST}',FEV1_FVC_POST='{patient.FEV1_FVC_POST}',FEV1_FVC_POST_PRED='{patient.FEV1_FVC_POST_PRED}',EXAM_FILE=(SELECT EXAM_FILE FROM (SELECT EXAM_FILE FROM LIFECHECK WHERE PRK=(SELECT MAX(E.PRK) FROM LIFECHECK E)) AS A) WHERE prk='{prk}'"
            row = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM LIFECHECK WHERE  DATE_EXAM IS NULL AND COST IS NULL")
            row = cursor.fetchone()
            messages.success(request, "Ο Ασθενής καταχωρήθηκε επιτυχώς!")

    return redirect(request.META['HTTP_REFERER'])



def exam_patient(request, prk='None'):
    insurance = Insurance.objects.all()
    exam = Exams.objects.all()
    context = {'insurance': insurance,
               'exam': exam,
               }
    if(prk != 'None'):
        patient = PatientExam.objects.get(prk=prk)
        context['patient'] = patient
    else:
        pass
    html_template = loader.get_template('home\exam_patient.html')
    return HttpResponse(html_template.render(context, request))


def load_pdf_exam_patient(request):
	pdf_link=request.GET.get('pdf_link', None)
	fdata = {}
	try:
		f = open(rf'C:\Users\chris\Desktop\python\django-datta-able\apps\static\assets\uploads\{pdf_link}', 'rb')
		pdf_reader = PyPDF2.PdfFileReader(f)
		pdf_reader.numPages
		page_one = pdf_reader.getPage(0)
		page_one_text = page_one.extractText()
		FVC = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))
		fdata['FVC_PRED'] = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[3]
		if(len(FVC)==13):
			fdata['FVC_BEST'] = list(
		page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[9]
		else:
			fdata['FVC_BEST'] = list(
		page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[7]
		if(len(FVC)>11):
			try:
				fdata['FVC_POST'] = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[5]
			except IndexError:
				fdata['FVC_POST'] = 0
			try:
				fdata['FVC_POST_PRED'] = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1/FVC')].split(' '))[6]
			except IndexError:
				fdata['FVC_POST_PRED']=0
		else:
			fdata['FVC_POST']=0
			fdata['FVC_POST_PRED']=0
		fdata['FEV1_PRED'] = list(
		page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[3]
		if(len(FVC)==13):
			fdata['FEV1_BEST'] = list(
		page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[8]
		else:
			fdata['FEV1_BEST'] = list(
		page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[7]
		if(len(FVC)>11):
			try:
				fdata['FEV1_POST'] = list(
        page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[5]
			except IndexError:
				fdata['FEV1_POST'] = 0
			try:
				fdata['FEV1_POST_PRED'] = list(
        page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[6]
			except IndexError:
				fdata['FEV1_POST_PRED']=0
		else:
			fdata['FEV1_POST']=0
			fdata['FEV1_POST_PRED']=0
		fdata['FEV1_FVC_PRED'] = list(
        page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[3]
		if(len(FVC)==13):
			fdata['FEV1_FVC_BEST'] = list(
		page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[8]
		else:
			fdata['FEV1_FVC_BEST'] = list(
		page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[7]
		if(len(FVC)>11):
			try:
				fdata['FEV1_FVC_POST'] = list(
        page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[5]
			except IndexError:
				fdata['FEV1_FVC_POST'] = 0
			try:
				fdata['FEV1_FVC_POST_PRED'] = list(
        page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[6]
			except IndexError:
				fdata['FEV1_FVC_POST_PRED']=0
		else:
			fdata['FEV1_FVC_POST']=0
			fdata['FEV1_FVC_POST_PRED']=0

	except:
		pass
	data = {
		'is_taken': pdf_link,
		'fdata': fdata
	}
	return JsonResponse(data)


def insert_patient(request):
    form = forminsert_patient(request.POST, request.FILES or None)
    if form.is_valid():
        try:
            form.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(request, "Ο Ασθενής καταχωρήθηκε επιτυχώς!")
    context = {'form': form}
    cost_patient()
    return redirect(request.META['HTTP_REFERER'])


def exam_patient_L(request,prk='None'):
    exam = Exams.objects.all().filter(code_exam__in=['x1','x2'])
    context = {'exam': exam}
    if(prk != 'None'):
        patient = lifecheck.objects.get(prk=prk)
        context['patient'] = patient
    else:
        pass
    html_template = loader.get_template('home\exam_patient_L.html')
    return HttpResponse(html_template.render(context, request))

def insert_patient_L(request):
    form = forminsert_patient_L(request.POST, request.FILES or None)
    if form.is_valid():
        try:
            form.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(request, "Ο Ασθενής καταχωρήθηκε επιτυχώς!")
    context = {'form': form}
    cost_patient_L()
    return redirect(request.META['HTTP_REFERER'])


def nurse_patient(request):
    insurance = Insurance.objects.all()
    exam = Exams.objects.all()
    context = {'insurance': insurance,
               'exam': exam}
    html_template = loader.get_template(
        '..\\templates\home\\nurse_patient.html')
    return HttpResponse(html_template.render(context, request))


def insert_patient2(request):
    form = forminsert_nurse(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(request, "Ο Ασθενής καταχωρήθηκε επιτυχώς!")
    context = {'form': form}
    return render(request, '..\\templates\home\\nurse_patient.html')


def cost_patient():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE patient_exam p set cost= round(cost_loop(cost,asfaleia),2) where cost like 'x%';")
        row = cursor.fetchone()


def cost_patient_L():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE lifecheck set cost= round((visit_price+if(energeia='x1',exam_price,0)),2) where cost like 'x%';")
        row = cursor.fetchone()


def invoice(request):
    #patient = PatientExam.objects.all()
    data = []
    cursor = connection.cursor()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where date_exam=curdate()')
    daily_revenue = cursor.fetchone()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where month(date_exam)=month(curdate())')
    monthly_revenue = cursor.fetchone()
    cursor.execute('select count(*) from patient_exam')
    total_visits_biokliniki = cursor.fetchone()
    cursor.execute('select count(*) from lifecheck')
    total_visits_lifecheck = cursor.fetchone()
    cursor.execute('select round(sum(cost),2) from patient_exam')
    total_revenue = cursor.fetchone()
    cursor = connection.cursor()
    invoice1 = PatientExam.objects.raw(
        'select cast(month(date_exam) as signed) prk,count(*) cnt,sum(cost) sum_cost,concat(month(date_exam),"/",year(date_exam)) period_exam,round(sum(cost)*0.2,2) fe,round(sum(cost)*0.8,2) payment,concat(month(date_exam),year(date_exam)) period from patient_exam group by concat(month(date_exam),"/",year(date_exam)) order by prk')
    for invoice in invoice1:
        chart = {'y': invoice.period_exam,
                 'a': invoice.cnt,
                 'b': invoice.sum_cost,
                 }
        data.append(chart)

    data2 = []
    exam = PatientExam.objects.raw(
        f'SELECT prk, energeia,date_exam FROM patient_exam order by date_exam')
    exams = Exams.objects.raw(f'SELECT code_exam,exam FROM exams')
    cost = Exam_cost.objects.raw('SELECT code_exam,COST_EXAM FROM EXAM_COST')
    dic_exams = {}
    for i in exams:
        dic_exams.update({i.code_exam: {"cost": 0.0, "title": ''}})

    for i in exams:
        dic_exams[i.code_exam]["title"] = i.exam

    for exam in exam:
        list_exam = exam.energeia.split(',')
        for litem in list_exam:
            for c in cost:
                if(c.code_exam) == litem:
                    dic_exams[c.code_exam]["cost"] += float(c.cost_exam)

    for i in dic_exams:
        chart2 = {
            'y': dic_exams[i]["title"],
            'a': dic_exams[i]["cost"]
        }
        data2.append(chart2)

    context = {'daily_revenue': daily_revenue,
               'monthly_revenue': monthly_revenue,
               'total_visits_biokliniki': total_visits_biokliniki,
               'total_visits_lifecheck': total_visits_lifecheck,
               'total_revenue': total_revenue,
               'invoice1': invoice1,
               'dic_exams': dic_exams
               }

    context['chart_data'] = json.dumps({
        'titles': 'Έσοδα Βιοκλινικής',
        'element': 'morris-bar-chart',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': ['a', 'b'],  # it can be custom
        'labels': ['Πλήθος Ασθενών', 'Έσοδα'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data2'] = json.dumps({
        'titles': 'Έσοδα ανά Εξέταση',
        'element': 'morris-bar-chart2',
        'data': data2,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 1,
        'resize': True,
        'responsive': True,
        'ykeys': ['a'],  # it can be custom
        'labels': ['Έσοδα'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    html_template = loader.get_template('home\invoice.html')
    return HttpResponse(html_template.render(context, request))

def invoice_L(request):
    #patient = PatientExam.objects.all()
    data = []
    cursor = connection.cursor()
    cursor.execute(
        'select round(sum(cost),2) from lifecheck where date_exam=curdate()')
    daily_revenue = cursor.fetchone()
    cursor.execute(
        'select round(sum(cost),2) from lifecheck where month(date_exam)=month(curdate())')
    monthly_revenue = cursor.fetchone()
    cursor.execute('select count(*) from patient_exam')
    total_visits_biokliniki = cursor.fetchone()
    cursor.execute('select count(*) from lifecheck')
    total_visits_lifecheck = cursor.fetchone()
    cursor.execute('select round(sum(cost),2) from lifecheck')
    total_revenue = cursor.fetchone()
    cursor = connection.cursor()
    invoice1 = lifecheck.objects.raw(
        'select cast(month(date_exam) as signed) prk,count(*) cnt,sum(cost) sum_cost,concat(month(date_exam),"/",year(date_exam)) period_exam,round(sum(cost)*0.2,2) fe,round(sum(cost)*0.8,2) payment,concat(month(date_exam),year(date_exam)) period from lifecheck group by concat(month(date_exam),"/",year(date_exam)) order by prk')
    for invoice in invoice1:
        chart = {'y': invoice.period_exam,
                 'a': invoice.cnt,
                 'b': invoice.sum_cost,
                 }
        data.append(chart)

    data2 = []
    exam = lifecheck.objects.raw(
        f'SELECT prk, energeia,date_exam FROM lifecheck order by date_exam')
    exams = Exams.objects.raw(f'SELECT code_exam,exam FROM exams')
    cost = Exam_cost.objects.raw('SELECT code_exam,COST_EXAM FROM EXAM_COST')
    dic_exams = {}
    for i in exams:
        dic_exams.update({i.code_exam: {"cost": 0.0, "title": ''}})

    for i in exams:
        dic_exams[i.code_exam]["title"] = i.exam

    for exam in exam:
        list_exam = exam.energeia.split(',')
        for litem in list_exam:
            for c in cost:
                if(c.code_exam) == litem:
                    dic_exams[c.code_exam]["cost"] += float(c.cost_exam)

    for i in dic_exams:
        chart2 = {
            'y': dic_exams[i]["title"],
            'a': dic_exams[i]["cost"]
        }
        data2.append(chart2)

    context = {'daily_revenue': daily_revenue,
               'monthly_revenue': monthly_revenue,
               'total_visits_biokliniki': total_visits_biokliniki,
               'total_visits_lifecheck': total_visits_lifecheck,
               'total_revenue': total_revenue,
               'invoice1': invoice1,
               'dic_exams': dic_exams
               }

    context['chart_data'] = json.dumps({
        'titles': 'Έσοδα Lifecheck',
        'element': 'morris-bar-chart',
        'data': data,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': ['a', 'b'],  # it can be custom
        'labels': ['Πλήθος Ασθενών', 'Έσοδα'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    context['chart_data2'] = json.dumps({
        'titles': 'Έσοδα ανά Εξέταση',
        'element': 'morris-bar-chart2',
        'data': data2,
        'xkey': 'y',
        'barSizeRatio': 0.70,
        'barGap': 1,
        'resize': True,
        'responsive': True,
        'ykeys': ['a'],  # it can be custom
        'labels': ['Έσοδα'],
        # it can be custom
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']
    }, default=str)

    html_template = loader.get_template('home\\invoice_L.html')
    return HttpResponse(html_template.render(context, request))

def invoice_L_analysis(request, period):
    year = period[-4:]
    month = period[:len(period)-4]
    cursor = connection.cursor()
    invoice = PatientExam.objects.raw(
        f"select prk,amka,name,surname,date_exam,energeia,cost from lifecheck where month(date_exam)='{month}' and year(date_exam)='{year}'")
    context = {'invoice': invoice}
    html_template = loader.get_template('home\\invoice_L_analysis.html')
    return HttpResponse(html_template.render(context, request))


def invoice_analysis(request, period):
    year = period[-4:]
    month = period[:len(period)-4]
    cursor = connection.cursor()
    exam={'x1':'Σπιρομέτρηση Απλή','x2':'Σπιρομέτρηση ΠΜ','x3':'Διαχ. Ικανότητα Πνεύμονος','x4':'Στατικοί Όγκοι','x5':'Οξυμετρία σε Ηρεμία','x6':'Οξυμετρία μετά Άσκησης','x7':'Καμπύλη Ροής προ μετά','x8':'Πνευμονολογική Εξέταση','x9':'Λήψη Αερίων Αίματος'}
    invoice = PatientExam.objects.raw(
        f"select prk,amka,name,surname,date_exam,energeia,cost,asfaleia from patient_exam where month(date_exam)='{month}' and year(date_exam)='{year}'")
    context = {'invoice': invoice}
    html_template = loader.get_template('home\\invoice_analysis.html')
    return HttpResponse(html_template.render(context, request))


def exam_table(request):
    patient = PatientExam.objects.all()
    cursor = connection.cursor()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where date_exam=curdate()')
    daily_revenue = cursor.fetchone()
    cursor.execute(
        'select round(sum(cost),2) from patient_exam where month(date_exam)=month(curdate())')
    monthly_revenue = cursor.fetchone()
    cursor.execute('select round(sum(cost),2) from patient_exam')
    total_revenue = cursor.fetchone()
    cursor.execute('select count(*) from patient_exam')
    total_visits_biokliniki = cursor.fetchone()
    cursor.execute('select count(*) from lifecheck')
    total_visits_lifecheck = cursor.fetchone()
    context = {'patient': patient,
               'daily_revenue': daily_revenue,
               'monthly_revenue': monthly_revenue,
               'total_revenue': total_revenue,
               'total_visits_biokliniki': total_visits_biokliniki,
               'total_visits_lifecheck': total_visits_lifecheck}
    html_template = loader.get_template('home\exam_table.html')
    return HttpResponse(html_template.render(context, request))


def exam_table_L(request):
    patient = lifecheck.objects.all()
    cursor = connection.cursor()
    cursor.execute(
        'select round(sum(cost),2) from lifecheck where date_exam=curdate()')
    daily_revenue = cursor.fetchone()
    cursor.execute(
        'select round(sum(cost),2) from lifecheck where month(date_exam)=month(curdate())')
    monthly_revenue = cursor.fetchone()
    cursor.execute('select round(sum(cost),2) from lifecheck')
    total_revenue = cursor.fetchone()
    cursor.execute('select count(*) from patient_exam')
    total_visits_biokliniki = cursor.fetchone()
    cursor.execute('select count(*) from lifecheck')
    total_visits_lifecheck = cursor.fetchone()
    context = {'patient': patient,
               'daily_revenue': daily_revenue,
               'monthly_revenue': monthly_revenue,
               'total_revenue': total_revenue,
               'total_visits_biokliniki': total_visits_biokliniki,
               'total_visits_lifecheck': total_visits_lifecheck}
    html_template = loader.get_template('home\exam_table_L.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def import_pdf(file):
    f = open(rf'C:\Users\chris\Desktop\python\django-datta-able\apps\static\assets\uploads\Evangelatos_Antonis.pdf', 'rb')
    fdata = {}
    pdf_reader = PyPDF2.PdfFileReader(f)
    pdf_reader.numPages
    page_one = pdf_reader.getPage(0)
    page_one_text = page_one.extractText()
    #Find FVC
    fdata['FVC'] = list(
    page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))
    fdata['FVC_Best'] = list(
    page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[9]
    fdata['FVC_Pred'] = list(
    page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[3]
    if(len(fdata['FVC'])>11):
        try:
            fdata['FVC_Post'] = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[5]
        except IndexError:
            fdata['FVC_Post']=0    
        try:
            fdata['FVC_Post_Pred'] = list(
        page_one_text[page_one_text.find('\nFVC'):page_one_text.find('\nFEV1')].split(' '))[6]
        except IndexError:
            fdata['FVC_Post_Pred']=0

    #Find FEV_1
    fdata['FEV1'] = list(
    page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))
    fdata['FEV1_Best'] = list(
    page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[9]
    fdata['FEV1_Pred'] = list(
    page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[3]
    if(len(fdata['FEV1'])>11):
        try:
            fdata['FEV1_Post'] = list(
        page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[5]
        except IndexError:
            fdata['FEV1_Post']=0
        try:
            fdata['FEV1_Post_Pred'] = list(
        page_one_text[page_one_text.find('\nFEV1'):page_one_text.find('\nFEV1/FVC')].split(' '))[6]
        except IndexError:
            fdata['FEV1_Post_Pred']=0    

    #Find FEV/FVC
    fdata['FEV1/FVC'] = list(
    page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))
    fdata['FEV1/FVC_Best'] = list(
    page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[9]
    fdata['FEV1/FVC_Pred'] = list(
    page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[3]
    if(len(fdata['FEV1/FVC'])>11):
        try:
            fdata['FEV1/FVC_Post'] = list(
        page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[5]
        except IndexError:
            fdata['FEV1/FVC_Post']=0
        try:    
            fdata['FEV1/FVC_Post_Pred'] = list(
            page_one_text[page_one_text.find('\nFEV1/FVC'):page_one_text.find('\nPEF')].split(' '))[6]
        except IndexError:
            fdata['FEV1/FVC_Post_Pred']=0
    return fdata



def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    day=request.POST.get('day')
    month=request.POST.get('month')
    year=request.POST.get('year')
    exam_table_data={}
    titles=['prk','amka','date_birth','name','father_name','phone','gender','surname','email','date_exam','allergies','asfaleia','apeikonistikos','baseline','cardio','close_relative_phone','conclusion','cost','current_disease','energeia','EQ5D5L','mmrc','istoriko','katoikon','gnomateusi','odigies','proliptikos','suggestion','tep','vaccine','family_history','FEV1_BEST','FEV1_FVC_BEST','FEV1_FVC_POST','FEV1_FVC_POST_PRED','FEV1_FVC_PRED','FEV1_POST','FEV1_POST_PRED','FEV1_PRED','FVC_BEST','FVC_POST','FVC_POST_PRED','FVC_PRE1','FVC_PRE2','FVC_PRE3','FVC_PRED','followup','ergastiriaka','exam_file']
 

    if( day!='' and year!='' and month!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where year(date_exam)='{year}' and month(date_exam)='{month}' and day(date_exam)='{day}'")
    elif(year!='' and month!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where year(date_exam)='{year}' and month(date_exam)='{month}' ")
    elif(year!='' and day!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where year(date_exam)='{year}' and day(date_exam)='{day}' ")
    elif(day!='' and month!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where day(date_exam)='{day}' and month(date_exam)='{month}' ")
    elif(day!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where day(date_exam)='{day}'")
    elif(month!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where month(date_exam)='{month}'")
    elif(year!=''):
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where year(date_exam)='{year}'")
    else:
        cursor = connection.cursor()
        exam_table_data = PatientExam.objects.raw(
        f"select * from patient_exam where prk='None'")
        exam_table_data.name='No parameters provided'

    response = HttpResponse(content_type='text/csv', )
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv";encoding="utf-8"'
    
    writer = csv.writer(response,delimiter=',')
    writer.writerow(titles)
    for data in exam_table_data:
        writer.writerow([data.prk,data.amka,data.date_birth,data.name,data.father_name,data.phone,data.gender,data.surname,data.email,data.date_exam,data.allergies,data.asfaleia,data.apeikonistikos,data.baseline,data.cardio,data.close_relative_phone,data.conclusion,data.cost,data.current_disease,data.energeia,data.EQ5D5L,data.mmrc,data.istoriko,data.katoikon,data.gnomateusi,data.odigies,data.proliptikos,data.suggestion,data.tep,data.vaccine,data.family_history,data.FEV1_BEST,data.FEV1_FVC_BEST,data.FEV1_FVC_POST,data.FEV1_FVC_POST_PRED,data.FEV1_FVC_PRED,data.FEV1_POST,data.FEV1_POST_PRED,data.FEV1_PRED,data.FVC_BEST,data.FVC_POST,data.FVC_POST_PRED,data.FVC_PRE1,data.FVC_PRE2,data.FVC_PRE3,data.FVC_PRED,data.followup,data.ergastiriaka,data.exam_file])

    return response


def agenta(request):
    today=date.today()
    all_events = Events.objects.all()
    get_event_types = Events.objects.only('event_type')

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:  
        event_arr = []
        if request.GET.get('event_type') == "all":
            all_events = Events.objects.all()
        else:   
            all_events = Events.objects.filter(event_type__icontains=request.GET.get('event_type'))

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.event_name
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {
        "events":all_events,
        "get_event_types":get_event_types,
        'date':today.strftime("%Y-%m-%d")

    }
    html_template = loader.get_template('home\\agenta.html')
    return HttpResponse(html_template.render(context,request))


def add_event(request):
    event_name=request.GET.get('event_name', None)
    start_date=request.GET.get('start_date', None)
    end_date=request.GET.get('end_date', None)
    event_type=request.GET.get('event_type', None)
    new_event = Events.objects.create(event_name=event_name, start_date=start_date, end_date=end_date, event_type=event_type)

    data = {
		'event_name': event_name,
        'start_date':start_date,
        'end_date':end_date,
        'event_type':event_type,
	}
    return JsonResponse(data)

def new_event(request):
    event_name=request.POST.get('event_name', None)
    start_date_f=request.POST.get('start_date', None)
    start_date = datetime.datetime. strptime(start_date_f, '%Y-%m-%dT%H:%M')
    end_date_f=request.POST.get('end_date', None)
    if(end_date_f==''):
        end_date_f=start_date_f
    event_type=request.POST.get('event_type', None)
    end_date = datetime.datetime. strptime(end_date_f, '%Y-%m-%dT%H:%M')
    new_event = Events.objects.create(event_name=event_name, start_date=start_date, end_date=end_date, event_type=event_type)

    data = {
		'event_name': event_name,
        'start_date':start_date,
        'end_date':end_date,
        'event_type':event_type,
	}
    return redirect(request.META['HTTP_REFERER'])

def update_event(request):
    event_id=request.GET.get('id')
    event = Events.objects.get(event_id=event_id)

    data = {
		'event_id': event.event_id,
		'event_name': event.event_name,
        'event_start': datetime.datetime.strptime(str(event.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M"),
        'event_end': datetime.datetime.strptime(str(event.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M"),
        'event_type': event.event_type,
	}
    return JsonResponse(data)

def update_event_form(request):
    event_id=request.POST.get('event_id2', None)
    event_name=request.POST.get('event_name2', None)
    start_date=request.POST.get('start_date2', None)
    end_date=request.POST.get('start_date2', None)
    event_type=request.POST.get('event_type2', None)

    if request.method=='POST' and 'updateev' in request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE events SET event_name='{event_name}',start_date='{start_date}',end_date='{end_date}',event_type='{event_type}' WHERE event_id='{event_id}'")
            row = cursor.fetchone()
    elif request.method=='POST' and 'deleteev' in request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                f"DELETE from events  WHERE event_id='{event_id}'")
            row = cursor.fetchone()
    return redirect(request.META['HTTP_REFERER'])


def some_view(request,prk):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    patient = PatientExam.objects.get(prk=prk)

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #data.prk,data.amka,data.date_birth,data.name,data.father_name,data.phone,data.gender,data.surname,data.email,data.date_exam,data.allergies,data.asfaleia,data.apeikonistikos,data.baseline,data.cardio,data.close_relative_phone,data.conclusion,data.cost,data.current_disease,data.energeia,data.EQ5D5L,data.mmrc,data.istoriko,data.katoikon,data.gnomateusi,data.odigies,data.proliptikos,data.suggestion,data.tep,data.vaccine,data.family_history,data.FEV1_BEST,data.FEV1_FVC_BEST,data.FEV1_FVC_POST,data.FEV1_FVC_POST_PRED,data.FEV1_FVC_PRED,data.FEV1_POST,data.FEV1_POST_PRED,data.FEV1_PRED,data.FVC_BEST,data.FVC_POST,data.FVC_POST_PRED,data.FVC_PRE1,data.FVC_PRE2,data.FVC_PRE3,data.FVC_PRED,data.followup,data.ergastiriaka,data.exam_file]
    p.drawString(8, 820,"Κωδικός Ασθενούς: "+ str(patient.prk) +"   Ονοματεπώνυμο: "+patient.name+" "+patient.surname+"     Πατρώνυμο: "+patient.father_name)
    p.drawString(8, 800," Ημ/νια Γέννησης: "+" "+patient.date_birth+"   "+" ΑΜΚΑ: "+ patient.amka +"    Ημ/νια Γέννησης: "+" "+patient.date_birth)
    p.drawString(8, 780, "Τηλέφωνο: "+patient.phone+"   e-mail: "+patient.email + " Τηλ. Πλησιέστερου Συγγενούς: "+patient.close_relative_phone)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')