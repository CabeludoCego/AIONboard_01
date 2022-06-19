from django.contrib import admin
#from django.contrib.auth import admin as auth_admin

# Register your models here.
# from .models import Produto, Venda
from .models import Produto, Venda
# Cart

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
  list_display = ('nome', 'preco_unitario', 
                  'estoque', 'imagem')

  list_filter = ['nome']

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
  list_display = ('nome', 'email', 'cpf' , 'endereco', 'valor_total')

  list_filter = ['nome']

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#   list_display = ('nome', 'email', 'cpf' , 'endereco', 'valor_total')

#   list_filter = ['nome']

# @admin.register(Produto)
# class ProdutoAdmin(auth_admin.UserAdmin):
#   form = EditarProduto
# #   add_form = CriarProduto

# @admin.register(User)
# class ProdutoAdmin(auth_admin.UserAdmin):
#   form = UserChangeForm
#   add_form = UserCreationForm