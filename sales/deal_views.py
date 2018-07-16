from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from fruit_sales import logging
from accounts.forms import LoginForm
from sales.forms import SalesDetailForm
from .models import Fruit,PriceRecord,SalesDetail
from django.views.generic import UpdateView,DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(redirect_field_name='cannot_access')
def add_deal(request):
    deal_form = SalesDetailForm(request.POST or None)
    if request.method == 'POST':
        fruit,quantity,deal_sum,deal_date = extract_parameters(request)
        if deal_form.is_valid():
            create_deal(request,fruit,quantity,deal_sum,deal_date)
            return redirect(reverse_lazy('sales:deals'))
        else:
            messages.error(request, "登録に失敗しました")
    base_title = '販売情報管理'
    base_url = '/top/deals'
    method_title = '新規登録'
    context = {'form': deal_form,'choice_fruit': Fruit.objects.all(),
            'base_title': base_title, 'base_url': base_url , 'method_title': method_title, }
    context['choice_minute'] = get_minute_box()
    return render(request, 'sales/add_deal.html',context)


def get_minute_box():
    minutes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
            51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    return minutes


def get_attributes(post,instance):
    quantity = post['quantity']
    deal_date = get_deal_date(post['input_date'],post['choice_time'],post['choice_minute'])
    if hasattr(instance,"price"):
        deal_sum = calc_deal_sum(instance.price,quantity)
    else:
        deal_sum = calc_deal_sum(instance.price_record.market_value,quantity)
    return quantity,deal_sum,deal_date


def extract_parameters(request):
    instance = Fruit.objects.get(pk = request.POST['choice_fruit'])
    quantity,deal_sum,deal_date = get_attributes(request.POST,instance)
    fruit = instance.name
    return fruit,quantity,deal_sum,deal_date


def get_deal_date(date,choice_time,choice_minute):
    if len(choice_minute) == 1:
        choice_minute = str(0) + choice_minute
    deal_date = str(date) + " " + str(choice_time) + ':' + str(choice_minute)
    return deal_date


def calc_deal_sum(price,quantity):
    deal_sum = int(price) * int(quantity)
    return deal_sum


def create_deal_try(fruit,quantity,deal_sum,deal_date):
    price_record_instance = PriceRecord.objects.filter(record_title=fruit).latest('regist_date')
    SalesDetail.objects.create( price_record = price_record_instance,
            quantity = quantity, deal_sum = deal_sum, input_date = deal_date.split(" ")[0], deal_date = deal_date)
    return True


def create_deal(request,fruit,quantity,deal_sum,deal_date):
    try:
        is_success = create_deal_try(fruit,quantity,deal_sum,deal_date)
    except:
        deal_form = SalesDetailForm()
        context = {'form': deal_form }
        return render(request, 'sales/add_deal.html',context)


class DealUpdateView(LoginRequiredMixin,UpdateView):
    model = SalesDetail
    template_name = 'sales/deal_update.html'
    form_class = SalesDetailForm
    success_url = '/top/deals'
    redirect_field_name = 'cannot_access'

    def get_object(self):
        instance = SalesDetail.objects.get(pk=self.kwargs['pk'])
        return instance


    def form_valid(self, form):
        instance = self.get_object()
        quantity,deal_sum,deal_date = get_attributes(self.request.POST,instance)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.pk = instance.pk
            detail.price_record = PriceRecord.objects.get(pk=instance.price_record.pk)
            detail.deal_sum = deal_sum
            detail.deal_date = deal_date
            detail.save()
            return redirect("sales:deals")

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.error(self.request, "更新に失敗しました")
        return super(DealUpdateView, self).form_invalid(form)


    def get_date_placeholder(self):
        pk = self.kwargs['pk']
        target_deal = SalesDetail.objects.get(pk=pk)
        pre_date_placeholder = str(target_deal.deal_date)
        date_placeholder = pre_date_placeholder.split(" ")
        return date_placeholder


    def get_context_data(self, **kwargs):
        context = super(DealUpdateView, self).get_context_data(**kwargs)
        base_title = '販売情報管理'
        base_url = '/top/deals'
        method_title = '編集'
        choice_minute = get_minute_box()
        date_placeholder = self.get_date_placeholder()
        page_info_context = { 'base_title': base_title, 'base_url': base_url,
                'date_placeholder': date_placeholder[0], 'choice_minute': choice_minute,
                'method_title': method_title }
        context.update(page_info_context)
        return context


class DealDeleteView(LoginRequiredMixin,DeleteView):
    model = SalesDetail
    form_class = SalesDetailForm
    template_name = 'sales/delete_confirm.html'
    success_url = reverse_lazy('sales:deals')
    redirect_field_name = 'cannot_access'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_title = '販売情報管理'
        base_url = '/top/deals'
        method_title = '削除'
        page_info_context = { 'base_title': base_title, 'base_url': base_url,
                'method_title': method_title, }
        context.update(page_info_context)
        return context

