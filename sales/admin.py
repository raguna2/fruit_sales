from django.contrib import admin
from .models import Fruit,PriceRecord,SalesDetail

# class FruitInline(admin.TabularInline):
#     model = Fruit
#     extra =3
#
#
# class SalesDetailInline(admin.StackedInline):
#     model = SalesDetail
#     extra = 3


class FruitAdmin(admin.ModelAdmin):
    fields = ['name','price']
    list_display =('id','name','price','regist_date')


class PriceRecordAdmin(admin.ModelAdmin):
    fields = ['record_title','market_value']
    list_display =('id','record_title','market_value','regist_date')


class SalesDetailAdmin(admin.ModelAdmin):
    fields = ['price_record','quantity','deal_sum','deal_date']
    list_display =('id','quantity','deal_sum','deal_date')
#
admin.site.register(Fruit,FruitAdmin)
admin.site.register(PriceRecord,PriceRecordAdmin)
admin.site.register(SalesDetail,SalesDetailAdmin)
