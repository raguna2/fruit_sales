from django.shortcuts import render,redirect
from fruit_sales import logging
from accounts.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from .models import Fruit
from .deal_views import create_deal_try


@login_required(redirect_field_name='cannot_access')
def after_login(request):
    username = str(request.user)
    return redirect('sales:mainpage')


@login_required(redirect_field_name='cannot_access')
def render_menu(request):
    if request.user.is_authenticated:
        return render(request, 'sales/mainpage.html')
    login_form = LoginForm(request.POST or None)
    context = { 'login_form': login_form }
    return render(request, 'registration/login.html',context)


def get_match_fruit():
    name_list = []
    fruits = Fruit.objects.all().distinct("name").select_related()
    for fruit in fruits:
        name_list.append(fruit.name)
    return name_list


def clean_dataframe(uploaded_file):
    match_fruit = get_match_fruit()
    df = pd.read_csv(uploaded_file, names=('fruit_name', 'quantity', 'deal_sum', 'deal_date'))
    df = df.dropna(how='any')
    df['quantity'] = df['quantity'].astype(int)
    df['deal_sum'] = df['deal_sum'].astype(int)
    date_pattern = '^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]$'
    df = df[df['deal_date'].str.match(date_pattern)]
    df = df[df['fruit_name'].isin(match_fruit)]
    return df


def get_deal_row_box(df):
    deal_row_box = []
    for index, row in df.iterrows():
        row_data = [row[0],row[1],row[2],row[3]]
        deal_row_box.append(row_data)
    logging.info(deal_row_box)
    return deal_row_box


@login_required(redirect_field_name='cannot_access')
def upload_csv(request):
    uploaded_file = request.FILES['resume']
    if str(uploaded_file).split('.')[1] == 'csv':
        df = clean_dataframe(uploaded_file)
        deal_row_box = get_deal_row_box(df)
        for elms in deal_row_box:
            is_success = create_deal_try(elms[0],elms[1],elms[2],elms[3])
        messages.success(request, 'アップロードが完了しました。')
    else:
        # csvファイルではない場合
        messages.error(request, "ファイルの拡張子はcsvでなければなりません。")
    return redirect("sales:deals")
