from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from fruit_sales import logging
from accounts.forms import LoginForm
from sales.forms import FruitForm
from .models import Fruit
from django.views.generic import UpdateView,DeleteView
from .models import PriceRecord
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from sales.views import get_match_fruit

@login_required(redirect_field_name='cannot_access')
def add_fruit(request):
    fruit_form = FruitForm(request.POST or None)
    context = get_add_fruit_context(fruit_form)
    if request.method == 'POST':#POSTの場合
        if fruit_form.is_valid():
            create_fruit(request,fruit_form)
            return redirect(reverse_lazy('sales:masters'))
        else:
            messages.error(request, "登録に失敗しました")#作成失敗したとき
            return render(request, 'sales/add_fruit.html',context)
    return render(request, 'sales/add_fruit.html',context)


def get_add_fruit_context(fruit_form):
    base_title = '果物マスタ管理'
    base_url = '/top/masters'
    method_title = '新規登録'
    context = {'form': fruit_form,'base_title': base_title,
            'method_title': method_title,'base_url': base_url }
    return context


def create_fruit(request, fruit_form):
    record_instance = create_record(request.POST['name'],request.POST['price'])
    new_fruit = fruit_form.save(commit=False)
    new_fruit.price_record = record_instance
    new_fruit.save()


def create_record(record_title,market_value):
    record_instance = PriceRecord.objects.create(record_title=record_title,market_value=market_value)
    return record_instance


class FruitUpdateView(LoginRequiredMixin,UpdateView):
    model = Fruit
    template_name = 'sales/fruit_update.html'
    form_class = FruitForm
    success_url = '/top/masters'
    redirect_field_name = 'cannot_access'

    def form_valid(self, form):
        name = self.request.POST['name']
        price = self.request.POST['price']
        record_instance = create_record(name,price)
        return super(FruitUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.error(self.request, "更新に失敗しました")
        return super(FruitUpdateView, self).form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_title = '果物マスタ管理'
        base_url = '/top/masters'
        method_title = '編集'
        page_info_context = {
                'base_title': base_title,
                'base_url': base_url,
                'method_title': method_title,
                }
        context.update(page_info_context)
        return context


class FruitDeleteView(LoginRequiredMixin,DeleteView):
    model = Fruit
    form_class = FruitForm
    template_name = 'sales/delete_confirm.html'
    success_url = reverse_lazy('sales:masters')
    redirect_field_name = 'cannot_access'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_title = '果物マスタ管理'
        base_url = '/top/masters'
        method_title = '削除'
        page_info_context = {
                'base_title': base_title,
                'base_url': base_url,
                'method_title': method_title,
                }
        context.update(page_info_context)
        return context

