from django import template
from django.db.models import Q
from calendar import Calendar
import datetime 
from datetime import date, timedelta
import re
from secretaria.models import agenda


register = template.Library()
 
@register.tag(name="get_calendar")
def do_calendar(parser, token):
    syntax_help = "syntax should be \"get_calendar for <month> <year> as <var_name>\""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments, %s" % (token.contents.split()[0], syntax_help)
    m = re.search(r'for (.*?) (.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments, %s" % (tag_name, syntax_help)
    return GetCalendarNode(*m.groups())
 
class GetCalendarNode(template.Node):
    def __init__(self, month, year, var_name):
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.var_name = var_name
        
    def render(self, context):
        mycal = Calendar()
        print mycal
        context[self.var_name] = mycal.monthdatescalendar(int(self.year.resolve(context)), int(self.month.resolve(context)))
        return ''

@register.filter(name="get_peticiones")
def get_peticiones(peticiones, dia):
    #return peticiones.filter(Q(creado_fecha__day=dia) | Q(inicio_fecha__day=dia) | Q(terminado_fecha__day=dia) | Q(completo_fecha__day=dia))

    return peticiones.filter(Q(fecha__day=dia))

# tag para el calendario personal de cada uno de los profesionales del centro
@register.tag(name="get_calendar_personal")
def do_calendar(parser, token):
    syntax_help = "syntax should be \"get_calendar_personal for <month> <year> as <var_name>\""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments, %s" % (token.contents.split()[0], syntax_help)
    m = re.search(r'for (.*?) (.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments, %s" % (tag_name, syntax_help)
    return GetCalendarNode(*m.groups())
 
class GetCalendarNode(template.Node):
    def __init__(self, month, year, var_name):
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.var_name = var_name
        
    def render(self, context):
        mycal = Calendar()
        context[self.var_name] = mycal.monthdatescalendar(int(self.year.resolve(context)), int(self.month.resolve(context)))
        return ''

@register.filter(name="get_peticiones")
def get_peticiones(peticiones, dia):
    #return peticiones.filter(Q(creado_fecha__day=dia) | Q(inicio_fecha__day=dia) | Q(terminado_fecha__day=dia) | Q(completo_fecha__day=dia))
    return peticiones.filter(Q(fecha__day=dia))

# de las funciones de meses de otro calendario
def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def cal_mes(year=date.today().year, month=date.today().month):

    event_list = agenda.objects.filter(fecha__year=year, fecha__month=month)
    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    cal_mes = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        for event in event_list:
            if day >= event.fecha.date() and day <= event.fecha.date():
                cal_day['event'] = True
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        week.append(cal_day)
        if day.weekday() == 6:
            cal_mes.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': cal_mes, 'headers': week_headers}

register.inclusion_tag('tags/cal_mes.html')(cal_mes)