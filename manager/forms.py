from django import forms
# from django.contrib.auth import forms
from .models import Produto, Cart, Venda

#PRODUCT_QUANTITY_CHOICES = [1, 2, 3, 4, 5]
PRODUCT_QUANTITY_CHOICES = [
    (i, str(i)) for i in range(1,21)
]

class CriarProduto(forms.ModelForm):
  class Meta:  # Com o Meta, não cria na raiz da classe
    model = Produto
    fields = ['nome', 'imagem', 'preco_unitario' , 'estoque']
  

class UpdateProduto(forms.ModelForm):
  class Meta:  
    model = Produto
    fields = ['nome', 'imagem', 'preco_unitario' , 'estoque']


class AdicionarCart(forms.Form):
  quantidade = forms.IntegerField(label="Quantidade")

class DadosVenda(forms.ModelForm):
  class Meta:
    model = Venda
    fields = ['nome', 'email', 'cpf' , 'endereco']

  # TypedChoiceField(
  #   label="Quantidade", coerce=int, 
  #   choices=PRODUCT_QUANTITY_CHOICES
  # )
  # override = forms.BooleanField(
  #   required= False, initial=False, widget=forms.HiddenInput
  # )


# class CriarProduto(forms.UserCreationForm):
#   class Meta(forms.CriarProduto.Meta):
#     model = Produto


# class EditarProduto(forms.UserChangeForm):
#   class Meta(forms.UserChangeForm.Meta):
#     model = Produto