from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware

from decimal import Decimal
import copy

from django.views.generic import View, TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CriarProduto, UpdateProduto, AdicionarCart, DadosVenda
from .models import Produto, Cart, Venda, cart


# import queries
class Index(ListView):
  template_name = 'index.html'
  model = Produto
  queryset = Produto.objects.all()
  # success_url = reverse_lazy('index')

class IndexM_View(TemplateView):
  template_name = 'manager/index_manager.html'


class ProdutoList(ListView): #,UpdateView):
  model = Produto
  queryset = Produto.objects.all()
  template_name = 'manager/manager_list.html'
  # success_url = reverse_lazy('manager:list')

# ------- com Forms simplificado --------------
class ProdutoCreate(SuccessMessageMixin,CreateView):
  model = Produto
  form_class = CriarProduto
  template_name = 'manager/manager_add.html'
  success_message = 'Produto adicionado com sucesso!'
  success_url = reverse_lazy('manager:add') #


class ProdutoUpdate(SuccessMessageMixin,UpdateView):
  model = Produto
  form_class = UpdateProduto
  template_name = 'manager/manager_att.html'
  success_message = 'Produto atualizado com sucesso!'
  success_url = reverse_lazy('manager:list')

## Catalogo e venda
class Catalogo(ListView):
  model = Produto
  paginate_by: 10
  template_name = 'venda/catalogo.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      produto = Produto.objects.all()
      # import pdb; pdb.set_trace()
      context['teste'] = 'Olá meu querido'
      return context


class ProdutoCompra(SuccessMessageMixin, DetailView):
  queryset = Produto.objects.filter(disponivel=True).all()
  extra_context = {"form": AdicionarCart()}
  template_name = 'venda/produto.html'
  success_url = reverse_lazy('venda/carrinho.html')
  success_message = 'Produto adicionado ao carrinho!'

class Sucesso(SuccessMessageMixin, TemplateView):
  model = Venda
  template_name = 'venda/sucesso.html'
  success_message = 'Compra realizada com sucesso!'


class Checkin(SuccessMessageMixin, CreateView):
  model = Venda
  form_class = DadosVenda
  template_name = 'venda/checkin.html'
  success_message = 'Compra efetuada com sucesso!'

  # Form preenchido: é assumido como a venda
  # Contudo faltam atributos a pegar do cart

  def form_valid(self,form):
    cart = Cart(self.request)
    if cart:   # se o carro existe:
      # import pdb; pdb.set_trace()
      venda = form.save()   # salva e define venda
      for item in cart:
        print(item)
        venda.valor_total += item['preco_total']
      cart.clear()
      return render(self.request, "venda/sucesso.html", {"venda": venda})
    return HttpResponseRedirect(reverse_lazy("manager:checkin"))

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      cart = Cart(self.request)
      preco_t = 0
      for key,values in cart.cart.items():
        # import pdb; pdb.set_trace()
        preco_t += float(values['preco']) * float(values['quantidade'])
      context['valorCarrinho'] = preco_t
      # Passar teste ao fim
      return context



##########################################

@require_POST
def cart_add(request, *args ,**kwargs):
  cart = Cart(request)
  produto_id = kwargs['pk']
  produto_obj = get_object_or_404(Produto, id=produto_id)
  # import pdb; pdb.set_trace()
  

  form = AdicionarCart(request.POST)
  if form.is_valid():
    cd = form.cleaned_data
    cart.add(
      produto=produto_obj,
      quant=cd["quantidade"],
    )
    return redirect("manager:cart")
  return render(request, "venda/catalog.html", {"produto": produto_obj})

@require_POST
def cart_remove(request, *args,**kwargs):
  cart = Cart(request)
  produto_id = kwargs['pk']
  produto_obj = get_object_or_404(Produto, id=produto_id)
  cart.remove(produto_obj)
  return redirect("manager:cart")

def cart_detail(request):
  cart = Cart(request)
  return render(request, "venda/carrinho.html", {"cart": cart})




# ---------- Sem forms ---------------
# class ProdutoCreate(CreateView):
#   model = Produto
#   fields = '__all__'
#   template_name = 'manager_add.html'
#   success_url = reverse_lazy('manager:add')

# class ProdutoUpdate(UpdateView):
#   model = Produto
#   template_name = 'manager_att.html'
#   fields = ['nome', 'preco_unitario' , 'estoque']
#   # success_url = ('/')
#   success_url = reverse_lazy('manager:list')







# Com forms - na raça
# class ProdutoCreate(View):
#   form_class = CriarProduto
#   initial = {'key':'value'}
#   template_name = 'manager_add.html'

#   def get(self, request, *args, **kwargs):
#     form = self.form_class(initial=self.initial)
#     return render(request, self.template_name, {'form':form})
  
#   def post(self,request, *args, **kwargs):
#     form = self.form_class(request.POST)
#     if form.is_valid():
#       # Salva o atual, e inicia um novo form.
#       produto = form.save()
#       form = CriarProduto() # apenas se for válido
#       context = {
#       'form': form
#       }
#       return render(request, "manager_add.html", context=context)
#     # Se não válido, guarda dados e mostra o form novamente
#     context = {
#       'form': form
#     }
#     return render(request, self.template_name, context)


# class ProdutoUpdate(FormView):
#   #model = Produto
#   form_class = UpdateProduto
#   template_name = 'manager_att.html'
#   fields = ['nome', 'estoque']

#   # form_class = UpdateProduto
#   initial = {'key':'value'}

#   def get_context(self, request, **kwargs):
#     context = super(ProdutoUpdate, self).get_context(**kwargs)
#     print(context)
#     data = context.objects.all()
#     context['queryset'] = data.filter(pk = request.GET.get("pk"))
#     print(context)
#     return context

#   def get(self, request, **kwargs):
#     form = self.form_class(request.GET.get(Produto.pk))
#     #(initial=self.initial)
#     return render(request, self.template_name, {'form':form})
  
#   def post(self,request, *args, **kwargs):
#     form = self.form_class(request.POST)
#     if form.is_valid():
#       # Salva o atual, e inicia um novo form.
#       produto = form.save()
#       return render(request, "manager_list.html")
#     # Se não válido, guarda dados e mostra o form novamente
#     context = {
#       'form': form
#     }
#     return render(request, self.template_name, context)
