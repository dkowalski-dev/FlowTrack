from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=30, blank=True, default="")
    company_name = models.CharField(max_length=255, blank=True, default="")
    nip = models.CharField(max_length=10, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=16, blank=True, default="")
    address = models.CharField(max_length=120, blank=True, default="")
    #Wyświetlanie listy ofert
    show_created = models.BooleanField(default=True)
    show_client = models.BooleanField(default=True)
    show_description = models.BooleanField(default=False)
    show_client_address = models.BooleanField(default=True)
    show_client_region = models.BooleanField(default=True)
    show_client_email = models.BooleanField(default=True)
    show_client_phone = models.BooleanField(default=True)
    show_status = models.BooleanField(default=True)

    #Paginacje na stronach
    offers_paginator = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    produtcs_paginator = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    categories_paginator = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    statuses_paginator = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    #Sortowanie na stronach
    offers_choices = (
        ('-created', 'Od najnowszych'),
        ('created', 'Od najstarszych'),
        ('status__name', 'Po statusie'),
        ('description', 'Po opisie'),
        ('region', 'Region'),
        ('client', 'Po nazwie klienta')
    )
    products_choices = (
        ('serial_number', 'Numer/Kod produktu'),
        ('-serial_number', 'Numer/Kod produktu odwrócone'),
        ('name', 'Nazwa'),
        ('-name', 'Nazwa od końca'),
        ('category__name', 'Kategorie'),
        ('-category__name', 'Kategorie odwrócone'),
        ('purchase_price', 'Cena zakupu malejąco'),
        ('-purchase_price', 'Cena zakupu rosnąco'),
        ('sale_price', 'Cena sprzedaży malejąco'),
        ('-sale_price', 'Cena sprzedaży rosnąco'),
    )
    categories_choices = (
        ('name', 'Nazwa'),
        ('-name', 'Nazwa od końca'),
        ('vat', 'Stawka VAT rosnąco'),
        ('-vat', 'Stawka VAT malejąco'),
    )
    statuses_choices = (
        ('name', 'Nazwa'),
        ('-name', 'Nazwa od końca'),
        ('type', 'Rodzaj'),
        ('-type', 'Rodzaj od końca'),
    )
    offers_sort = models.CharField(max_length=20, choices=offers_choices, default='-created')
    products_sort = models.CharField(max_length=20, choices=products_choices, default='name')
    categories_sort = models.CharField(max_length=20, choices=categories_choices, default='name')
    statuses_sort = models.CharField(max_length=20, choices=statuses_choices, default='name')
