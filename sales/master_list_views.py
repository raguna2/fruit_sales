from django.views.generic import ListView
from django.shortcuts import render
from sales.models import Fruit
from fruit_sales import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class MasterListView(LoginRequiredMixin,ListView):
    model = Fruit
    context_object_name = "lists"
    template_name = 'sales/master.html'
    redirect_field_name = 'cannot_access'

    def get_queryset(self):
        fruits = Fruit.objects.all().order_by('id').reverse()
        return fruits

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_title = '果物マスター管理'
        table_header = ['ID','名称','単価','登録日時','','']
        page_info_context = {
                'base_title': base_title,
                'table_header': table_header,
                }
        context.update(page_info_context)
        return context
