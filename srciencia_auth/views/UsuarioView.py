from django.shortcuts import render, redirect
from srciencia_auth.models import Usuario
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

