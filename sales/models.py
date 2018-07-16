from django.db import models
from django.conf import settings
from django.contrib.admin import widgets
from django.core.validators import MinValueValidator,RegexValidator
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from fruit_sales import logging
import re

def validate_num(value):
    if re.search("^!+$", '!'):
        raise ValidationError( _('個数に数字以外のものが含まれています。'))

class PriceRecord(models.Model):
    record_title = models.CharField(max_length = 64)
    market_value = models.PositiveIntegerField(default="1")
    regist_date = models.DateTimeField(auto_now_add = True)

class Fruit(models.Model):
    name = models.CharField(max_length = 64)
    price = models.PositiveIntegerField(
            default="1",
            validators=[
                MinValueValidator(1,message='単価は0円以上にしてください。'),
                RegexValidator(regex='^[1-9]{1}\d*$', message='価格は金額のみを入力してください。')],
            )
    regist_date = models.DateField(
            auto_now_add = True,
            validators=[
                RegexValidator(
                    # ex.2018-03-08 15:01
                    regex='^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]$',
                    message='表示形式に誤りがあります。'
                    ),
                ],
            )
    price_record = models.ForeignKey(PriceRecord,on_delete=models.DO_NOTHING,
                                     related_name='price_record',blank=True, null=True)


    class Meta:
        verbose_name = 'fruit'
        verbose_name_plural = 'fruits'

    def __str__(self):
        return self.name


class SalesDetail(models.Model):
    price_record = models.ForeignKey(PriceRecord,on_delete=models.DO_NOTHING,related_name='fruit_name')
    quantity = models.PositiveIntegerField(
            default="1",
            validators=[
                RegexValidator(
                    regex='^[1-9]\d*$',
                    message='個数は0個以上でかつ0から始まらないようにしてください。',
                    code='invalid_quantity'
                    ),
                ],
            )
    deal_sum = models.PositiveIntegerField(blank=True)
    input_date = models.DateField(blank=True)
    deal_date = models.DateTimeField(validators=[
                RegexValidator(
                    regex='^[0-9]{4}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])$',
                    message='日時の形式が間違っています。',
                    code='invalid_datetime'
                    ),
                ],
                )

    class Meta:
        verbose_name = 'sales_detail'
        verbose_name_plural = 'sales_details'

    def __str__(self):
        return str(self.deal_sum)

