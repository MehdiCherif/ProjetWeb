#-*- coding : utf-8 -*-
from django import forms
from django.forms.models import modelform_factory
from gestionAbsence.models import *

modelform_factory(Justificatif, 
	fields=(""), 
	widget={},
	labels={})