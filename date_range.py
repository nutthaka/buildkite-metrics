#!/usr/bin/env python3

from datetime import date, timedelta
from string import Template

def get_date_tuples(number_of_days):
    today = date.today()
    template = Template('${day}T00:00:00+1000')
    date_tuples = []

    for delta in reversed(range(0, number_of_days)):
        dateFrom = template.substitute(day=today - timedelta(days=delta))
        dateTo = template.substitute(day=today - timedelta(days=delta-1))
        date_tuples.append((dateFrom, dateTo))
    
    return date_tuples
    