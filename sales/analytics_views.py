from django.shortcuts import render,redirect
from fruit_sales import logging
from .models import SalesDetail
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
# 最終的な形
# monthly_details = [
#         {'month': "2018-07","sales": 19000 ,"breakdown": "ブルーベリー:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
#         {'month': "2018-06","sales": 13000 ,"breakdown": "ブルーベリー2:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
#         {'month': "2018-05","sales": 12000 ,"breakdown": "ブルーベリー3:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
#         ]
@login_required(redirect_field_name='cannot_access')
def render_analytics(request):
    base_title = '販売統計情報'
    df = make_target_df()
    monthly_details = get_monthly_details(df)
    daily_details = get_daily_details(df)
    context = { 'base_title': base_title, 'total': df['deal_sum'].sum(),
                'monthly_details': monthly_details, 'daily_details': daily_details }
    return render(request, 'sales/analytics.html',context)


def make_target_df():
    day_index = []
    pandas_box = []
    for i in SalesDetail.objects.all().select_related():
        quantity = i.quantity
        fruit_name = i.price_record.record_title
        deal_sum = i.deal_sum
        ymd = str(i.deal_date).split("+")[0]
        # DBにはUTCで登録されているので集計の際にはTZをAsia/Tokyoに変換する。
        day_index.append(pd.to_datetime(ymd,utc=True).tz_convert('Asia/Tokyo'))
        pandas_box.append([fruit_name, quantity, deal_sum ])
    df = pd.DataFrame( pandas_box, columns=['fruit_name', 'quantity','deal_sum'],index=day_index)
    return df


def get_last_three_month(target):
    display_months = []
    for i in range(0,3):
        first_of_month = target + relativedelta(day=1)
        # ex. 2018-08-08 -> 2018-08 "-" 08
        month = str(first_of_month).rsplit('-',1)[0]
        display_months.append(month)
        target = first_of_month - timedelta(days=1)
    return display_months


def get_last_three_day(target):
    display_days = [str(target)]
    for i in range(0,2):
        past_day = target - timedelta(days=1)
        display_days.append(str(past_day))
        target = past_day
    return display_days


def get_breakdown_full_text(fruit_by):
    breakdown_box = []
    for index, row in fruit_by.iterrows():
        # quantity は row[0]  deal_sum は row[1]が該当
        breakdown_text = index + ':' + str(row[1]) + '円' + '(' + str(row[0]) + ')'
        breakdown_box.append(breakdown_text)
    breakdown_fulltext = ' '.join(breakdown_box)
    return breakdown_fulltext


def get_details(df,detail_box,target_index,time_range):
    for index in target_index:
        fruit_by = df[index].groupby(pd.Grouper('fruit_name'))['quantity','deal_sum'].sum()
        # ↑ 果物毎の集計. 果物の売り上げを全て合計した結果 が fruit_by['deal_sum'].sum()
        sales = fruit_by['deal_sum'].sum()
        breakdown = get_breakdown_full_text(fruit_by)
        this_dict = { time_range : index, 'sales': sales , 'breakdown': breakdown }
        detail_box.append(this_dict)
    return detail_box


def get_monthly_details(df):
    monthly_details = []
    display_months = get_last_three_month(date.today())
    time_range = 'month'
    monthly_details = get_details(df,monthly_details,display_months,time_range)
    return monthly_details


def get_daily_details(df):
    daily_details = []
    display_days = get_last_three_day(date.today())
    time_range = 'day'
    daily_details = get_details(df,daily_details,display_days,time_range)
    return daily_details
