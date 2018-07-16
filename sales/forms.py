from django.forms import ModelForm,DateInput,TextInput,DateTimeInput
from sales.models import Fruit,SalesDetail
from django.contrib.admin import widgets
from fruit_sales import logging
from django.core.validators import ValidationError
import re
from django import forms
from django.core.validators import RegexValidator
from fruit_sales import settings


class FruitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FruitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "名称"
        self.fields['price'].label = "単価"


    class Meta:
        model = Fruit
        fields = ('name','price',)
        widgets = {
                'name': TextInput(
                    attrs={
                        'class':'input is-medium',
                        'placeholder':'名称'
                        }),
                'price': TextInput(
                    attrs={
                        'class':'input is-medium',
                        'placeholder':'単価'
                        }),
                    }



class SalesDetailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesDetailForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = "個数"
        self.fields['input_date'].label = "日時"

    def clean(self):
        cleaned_data = super(SalesDetailForm, self).clean()
        return cleaned_data

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if not re.search(r'^\d+',str(quantity)):
           self.add_error('quantity', '個数に数字以外の文字列が含まれている可能性があります。')
        if re.search(r'^0.+',str(quantity)):
           self.add_error('quantity', '個数は0を先頭に始まりません。')
        return quantity

    def clean_input_date(self):
        input_date = self.cleaned_data['input_date']
        if not str(input_date) == 'None':
            date_split = str(input_date).split('-')
        else:
            date_split = '2018-09-09'.split('-')
            raise forms.ValidationError("日付を入力してください。")
        if int(date_split[0]) < 1900:
            raise forms.ValidationError("売上年が古すぎます。1900年以前は入力できません。")
        if 2050 < int(date_split[0]):
            raise forms.ValidationError("売上年が新しすぎます。2050年以降は入力できません。")
        return input_date


    class Meta:
        model = SalesDetail
        fields = ('quantity','input_date')
        widgets = {
                'quantity': TextInput(
                    attrs={
                        'class':'input is-medium',
                        'placeholder':'個数'
                        }
                    ),
                'input_date': DateInput(
                    attrs={
                        'class':'input',
                        'id':'datepickerDemo2',
                        'type':'date',
                        'name':'date',
                        'value':'',
                        },
                    format=settings.DATE_INPUT_FORMATS,
                    ),
                  }
