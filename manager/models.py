from django.db import models
from django.utils.timezone import now
import uuid
import copy
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.test import TestCase
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.postgres.fields import ArrayField
from django.http import HttpRequest

from localflavor.br.models import BRCPFField

import datetime

import json

class Produto(models.Model):
  nome = models.CharField('Nome do Produto',blank=False, null=False, max_length=200)
  imagem = models.ImageField('Imagem',blank=True, null=True, upload_to='imgs')
  preco_unitario = models.DecimalField('Preço unitário',blank=False, null=False, max_digits=8, decimal_places=2)
  estoque = models.IntegerField('Estoque',blank=False, null=False,
  validators=[
    MinValueValidator(1)
    ]
  )
  disponivel = models.BooleanField(default=True)

  def __str__(self):
    return self.nome
  
  def __date__(self):
    self.data = datetime.now()
    return self.data

  def save(self, *args, **kwargs):
    if self.estoque <= 0:
      self.disponivel = False
    else:
      self.disponivel = True
    return super(Produto, self).save(*args, **kwargs)

#################################################3

class Cart():
  def __init__(self,request):
    if request.session.get("cart") is None:
      request.session["cart"] = {}
    self.cart = request.session["cart"]
    self.session = request.session

  def __iter__(self):
    cart = copy.deepcopy(self.cart)
    produtos = Produto.objects.filter(id__in=cart)
    for product in produtos:
      cart[str(product.id)]["produto"] = product

    # import pdb; pdb.set_trace()
    for item in cart.values():
      item["preco"] = Decimal(item["preco"])
      item["preco_total"] = item["preco"] * item["quantidade"]
      yield item

  def __len__(self):
    lenT = sum(item["quantidade"] for item in self.cart.values())
    return lenT

  def get_preco_total(self):
    preco_total = sum((Decimal(item["preco"]) * item["quantidade"]) for item in self.cart.values())
    #import pdb; pdb.set_trace()
    return preco_total


  def add(self, produto, quant=1):
    # import pdb; pdb.set_trace()
    product_id = str(produto.id)
    if product_id not in self.cart:
      self.cart[product_id] = {
        "quantidade" : quant,
        "preco": str(produto.preco_unitario)
      }
    else: 
      #import pdb; pdb.set_trace()
      if ((produto.estoque) > (quant + (self.cart[product_id]["quantidade"])) ): 
        # Quantidade maior que estoque
        self.cart[product_id]["quantidade"] += quant
    self.save()
  
  def remove(self, produto):
    product_id = str(produto.id)
    if product_id in self.cart:
      del self.cart[str(product_id)]
      self.save()
  
  def save(self):
    self.session.modified = True

  def clear(self):
    del self.session[settings.CART_SESSION_ID]
    self.save()

############################################################

class Venda(models.Model):
  nome = models.CharField('Cliente',blank=False, null=False, max_length=150)
  email = models.EmailField('E-mail',blank=False, null=False, max_length=120)
  
  endereco = models.TextField('Endereço',blank=False, null=False, max_length=300)
  data_criacao = models.DateField('Data de criação', auto_now_add=True)
  # cpf = models.BRCPFFIELD
  cpf = models.IntegerField('CPF sem espaços',blank=False, null=False, 
    validators=[
      MinValueValidator(00000000000),
      MaxValueValidator(99999999999)
      ]
    )
  # Valores atribuídos por métodos
  # produtos_comprados = ArrayField(
  #           models.IntegerField(blank=False, null=True),
  #           size=20, null=True
  #       )
  # qtds_compradas = ArrayField(
  #           models.IntegerField(blank=False, null=True),
  #           size=20, null=True
  #       )
  # qtds_compradas = models.CharField(max_length=300)
  valor_total = models.DecimalField('Valor total',blank=False, null=False, 
  max_digits=8, decimal_places=2, default=0)

  def __str__(self):
      return self.nome


# class ProdutosComprados()

   
  # def post_valor_total(self,*args, **kwargs):
  #   self.valor_total = sum((item["preco_total"]) for item in cart.values())
  #   print(self.valor_total)
  #   import pdb; pdb.set_trace()
  #   return super(Venda, self).save(*args, **kwargs)

  #import pdb; pdb.set_trace()

#   quantidade = models.IntegerField(blank=False, null=False, default=1)
#   valorTotal = models.FloatField(blank=False, null=False, editable=False, value={quantidade * Produto.preco_unitario})


#   def __str__(self):
#     return self.nome
    
def dummy_get_response(request):
    return None

def http_request():
  request = HttpRequest()
  middleware = SessionMiddleware(dummy_get_response)

def session(http_request):
    return http_request.session

def cart(http_request, session):
    cart = Cart(http_request)
    session.modified = False
    return cart
