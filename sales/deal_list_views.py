from django.views.generic import ListView
from sales.models import SalesDetail
from fruit_sales import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy


class DealListView(LoginRequiredMixin,ListView):
    model = SalesDetail
    context_object_name = "lists"
    template_name = 'sales/deals.html'
    redirect_field_name = 'cannot_access'


    def get_queryset(self):
        deals = SalesDetail.objects.all().order_by('deal_date').reverse()
        return deals


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_title = '販売情報管理'
        table_header = ['果物','個数','売上','販売日時','','']
        page_info_context = {
                'base_title': base_title,
                'table_header': table_header,
                }
        context.update(page_info_context)
        return context

