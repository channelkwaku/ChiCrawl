from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django import forms
from datetime import datetime
from django.db import models
from models import Bar, Address
from search import search
import sys
import csv
import os
import json

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

NEIGHBOR_FILE = os.path.join(RES_DIR, 'neighborhood.csv')
NEIGHBOR_COOR = os.path.join(RES_DIR, 'neighbor_coord.json')

def load_column(filename):
    with open(filename) as f:
        col = []
        for row in csv.reader(f):
            col.append(row[0])
    return col


def build_dropdown(options):
    #Convers a list to (value, label) tuples for <option> tag
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

NEIGHBOR = build_dropdown([None] + load_column(NEIGHBOR_FILE))

def get_origin_coord(filename, key):
    with open(filename) as f:
        data = json.load(f)
    lat = data[key]['location']['latitude']
    lon = data[key]['location']['longitude']
    return [lat, lon]

# Create your views here.
class ChicagoNeighbor(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.ChoiceField(label='Neighborhood', choices=NEIGHBOR, required=False))
        super(ChicagoNeighbor, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, values):
        if len(values) == 2:
            if values[0] is None or not values[1]:
                raise forms.ValidationError("Must specify both.")
            if values[0] < 0:
                raise forms.ValidationError("Walking time must be non-negative.")
        return values


class SearchForm(forms.Form):
    search = forms.CharField(label='Search terms', required=False)
    num_bars = forms.IntegerField(label='Number of bars to visit', required=False)
    neighborhood = ChicagoNeighbor(
           label='Distance/Neighborhood',
           help_text='e.g. 2 miles within Hyde Park',
           required=False,
           widget=forms.widgets.MultiWidget(
                    widgets=(forms.widgets.NumberInput,
                             forms.widgets.Select(choices=NEIGHBOR))))
    show_args = forms.BooleanField(label='Show_form_values', required=False)
    
def home(request):
    c = {}
    coord = []
    query = None # our query function (from a python file)
    #now = datetime.now()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        # Check if it's valid
        if form.is_valid():
            # convert form data to an args dictiionary
            args = {}
            if form.cleaned_data['search']:
                args['terms'] = form.cleaned_data['search']
            if form.cleaned_data['num_bars']:
                args['bar_num'] = form.cleaned_data['num_bars']
            neighbor = form.cleaned_data['neighborhood']
            #coord = get_origin_coord(NEIGHBOR_COOR, neighbor[1])
            if neighbor:
                args['distance'] = neighbor[0]
                args['neighbor'] = neighbor[1]
                coord = get_origin_coord(NEIGHBOR_COOR, args['neighbor'])
            if form.cleaned_data['show_args']:
                c['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)
           
            if len(coord) == 0:
                print('Exception caught')
                query = None 
            else:
                query = search(args, coord[0], coord[1])
            #except Exception as e:
                #print('Exception caught')
                #query = None
                
    else:
        form = SearchForm()
    if query is None:
        c['result'] = None
    else:
        # list of tuples [(name, lon, lat, weight, distance),..]
        result = query
        c['result'] = result
        # parameters for starting location/js
        c['origin_lat'] = coord[0]
        c['origin_lon'] = coord[1]
        # parameters for directions
        c['lat_list'] = get_lat(result)
        c['lon_list'] = get_lon(result) 
        print get_lat(result)
        print get_lon(result)
    
    c['form'] = form

    return render(request, 'index.html', c)

def get_lon(result):
    lon = []
    i = 0
    for value in result:
        lon.append(value[1])
        i = i + 1
        if i == 5:
            break
    return lon

def get_lat(result):
    lat = []
    i = 0
    for value in result:
        lat.append(value[2])
        i = i + 1
        if i == 5:
            break
    return lat

def result(request):
    c = {}
    #c['result'] = [1,2,3,4,5,6,7]
    return render(request, 'result.html', c)
    


