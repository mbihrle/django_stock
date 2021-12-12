import requests
import json

from django.shortcuts import redirect, render
from django.contrib import messages

import configparser
from .models import Stock
from .forms import StockForm

# Create your views here.
config = configparser.ConfigParser()
config.read('../../../_configs/config.ini')
API_KEY = config['iexcloud.io']['API_KEY']


def home(request):

    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']

        request_string = "https://cloud.iexapis.com/stable/stock/" + \
            ticker + "/quote?token=" + API_KEY

        api_request = requests.get(request_string)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error!"
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker_message': "Enter a Ticker Symbol Above..."})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            request_string = "https://cloud.iexapis.com/stable/stock/" + \
                str(ticker_item) + "/quote?token=" + API_KEY
            api_request = requests.get(request_string)
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error!"
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
