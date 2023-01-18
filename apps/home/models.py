# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.forms import ModelForm
from mirage import fields


class PatientExam(models.Model):
    prk = models.AutoField(primary_key=True)
    name = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    surname = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    date_birth = models.CharField(max_length=45, blank=True, null=True)
    asfaleia = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    energeia = models.CharField(max_length=2045, blank=True, null=True)
    date_exam = models.CharField(max_length=45, blank=True, null=True)
    istoriko = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    gnomateusi = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    odigies = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    cost = models.CharField(max_length=45, blank=True, null=True)
    amka = fields.EncryptedCharField(max_length=245, blank=True, null=True)
    gender = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    #exam_file = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    exam_file=models.FileField(null=True, blank=True, upload_to='apps/static/assets/uploads')
    FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_PRE1 = models.CharField(max_length=45, blank=True, null=True)
    FVC_PRE2 = models.CharField(max_length=45, blank=True, null=True)
    FVC_PRE3 = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_BEST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_BEST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_POST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_BEST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    father_name = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    phone = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    close_relative_phone = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    current_disease = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    family_history = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    allergies = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    vaccine = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    baseline = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    ergastiriaka = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    tep = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    katoikon = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    mmrc = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    EQ5D5L = fields.EncryptedCharField(max_length=245, blank=True, null=True)
    cardio = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    apeikonistikos = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    suggestion = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    conclusion = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    followup = fields.EncryptedTextField(max_length=2045, blank=True, null=True)
    email = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'patient_exam'


class PatientHosp(models.Model):
    prk = fields.EncryptedCharField(primary_key=True)
    name = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    age = fields.EncryptedCharField(max_length=3, blank=True, null=True)
    asfaleia = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    energeia = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    datein = models.CharField(max_length=45, blank=True, null=True)
    dateout = models.CharField(max_length=45, blank=True, null=True)
    personal_patient = models.BooleanField(blank=False, null=False)
    istoriko = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    gnomateusi = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    odigies = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    cost = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    payment = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    amka = fields.EncryptedCharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_hosp'


class Exams(models.Model):
    code_exam = models.CharField(primary_key=True, max_length=45)
    exam = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exams'

class Exam_cost(models.Model):
    code_exam = models.CharField(primary_key=True, max_length=45)
    cost_exam =  models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_cost'

class Insurance(models.Model):
    code_ins = models.AutoField(primary_key=True)
    insurance = fields.EncryptedCharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insurance'


class lifecheck(models.Model):
    prk = models.AutoField(primary_key=True)
    name = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    surname = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    date_birth = models.CharField(max_length=45, blank=True, null=True)
    energeia = models.CharField(max_length=2045, blank=True, null=True)
    date_exam = models.CharField(max_length=45, blank=True, null=True)
    istoriko = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    gnomateusi = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    odigies = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    cost = models.CharField(max_length=45, blank=True, null=True)
    amka = fields.EncryptedCharField(max_length=245, blank=True, null=True)
    gender = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    visit_price = models.CharField(max_length=45, blank=True, null=True)
    exam_price = models.CharField(max_length=45, blank=True, null=True)
    #exam_file = fields.EncryptedCharField(max_length=45, blank=True, null=True)
    exam_file=models.FileField(null=True, blank=True, upload_to='apps/static/assets/uploads')
    FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FVC_BEST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_BEST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_POST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_PRED = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_BEST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_POST = models.CharField(max_length=45, blank=True, null=True)
    FEV1_FVC_POST_PRED = models.CharField(max_length=45, blank=True, null=True)
    father_name = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    phone = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    close_relative_phone = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    current_disease = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    family_history = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    allergies = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    vaccine = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    baseline = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    ergastiriaka = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    tep = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    katoikon = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    mmrc = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    EQ5D5L = fields.EncryptedCharField(max_length=245, blank=True, null=True)
    cardio = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    apeikonistikos = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    suggestion = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    conclusion = fields.EncryptedCharField(max_length=2045, blank=True, null=True)
    followup = fields.EncryptedCharField(max_length=2045, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'lifecheck'

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    event_type = models.CharField(max_length=45,null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'events'

    def __str__(self):
        return self.event_name

