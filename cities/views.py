from open311_comparison import app
from flask import render_template, url_for, redirect
from cities.form import NewCityForm
from cities.models import City
from cities.models import ViewTypes
from open311_comparison import db, app

import os

import pandas as pd
import dateutil.parser
from dateutil import tz
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

@app.route('/')
@app.route('/index')
def index():
    cities = City.query.all()
    form = NewCityForm()
    return render_template('city/list_cities.html', cities=cities, form=form, view_types = ViewTypes)

@app.route('/add', methods=('GET','POST'))
def add_city():
    form = NewCityForm()
    if form.validate_on_submit():
        open311_endpoint = form.open311_endpoint.data 
        name = form.name.data
        open311_jurisdiction = form.open311_jurisdiction.data
        new_city = City(name,open311_endpoint,open311_jurisdiction)
        db.session.add(new_city)
        db.session.commit()
        return redirect(url_for('success'))
    else: 
        return render_template('city/add_city.html', form=form)
    
@app.route('/success')
def success():
    return "City registered"
    

@app.route('/view')
@app.route('/view/<city_name>')
@app.route('/view/<city_name>/<view_type>')
def city_matrix(city_name, view_type=''):
    if city_name == None:
        return redirect(url_for('index'))
 
    city = City.query.filter_by(name=city_name).first()
    if city == None:
        return "Did not find you city"
        
    create_view(city.name, city.open311_endpoint, jurisdiction=city.open311_jurisdiction, view_type=view_type)
    
    return render_template('city/city_matrix.html', city=city, view_type=view_type)
    
    

def create_view(city,open311_endpoint,jurisdiction, view_type=''):
    
    if open311_endpoint[-1] != '/':
        open311_endpoint = open311_endpoint+'/'
    
    url_requests = open311_endpoint + 'requests.json?start_date=2010-01-01T00:00:00Z'
    url_services = open311_endpoint + 'services.json'
    
    if jurisdiction != None:
        url_requests = url_requests+'&'+jurisdiction
        url_services = url_services+'&'+jurisdiction
            
    reports = pd.read_json(url_requests)
    services = pd.read_json(url_services)
    
    reports['requested_datetime'] = pd.to_datetime(reports['requested_datetime'])
    
    ax1 = plt.subplots()
    
    
    if (view_type == 'heatmap' or view_type == ''):
        reports['requested_weekday']=reports['requested_datetime'].dt.weekday
        weekdaynames = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        
        service_heatmap = pd.DataFrame(index=services['service_name'])
        
        for day,dayname in enumerate(weekdaynames):
            service_heatmap[dayname]=(reports['service_name'].where(reports['requested_weekday'] == day).value_counts())
            
        ax1 = sns.heatmap(service_heatmap,annot=True,linewidths=.5, annot_kws={"size": 10}, cbar=False)
        
    if (view_type == 'hour_heatmap'):
        if city == 'Maputo':
            reports['requested_hour']=reports['requested_datetime'].dt.hour+2
        else:
            reports['requested_hour']=reports['requested_datetime'].dt.hour
            
        service_heatmap = pd.DataFrame(index=services['service_name'])
        
        for hour in range(24):
            service_heatmap[hour]=(reports['service_name'].where(reports['requested_hour'] == hour).value_counts())
            
        ax1 = sns.heatmap(service_heatmap, cbar=True, cbar_kws={"orientation": "horizontal"})
    

    elif view_type == 'hours':
        reports['requested_day_time']=reports['requested_datetime'].dt.hour + reports['requested_datetime'].dt.minute / 60 + reports['requested_datetime'].dt.second / 3600
        ax1 = sns.stripplot(y="service_name", x="requested_day_time", data=reports)
        plt.xlim((0,24))
    
    elif view_type == 'days':
        reports['requested_day']=reports['requested_datetime'].dt.day
        ax1 = sns.violinplot(y="service_name", x="requested_day", data=reports,  bw=.1, scale="count")
        plt.xlim((0,31))
    
    plt.gcf().subplots_adjust(left=0.3)

    plt.savefig(os.path.join(app.config['STATIC_FOLDER'], city+'_'+view_type+'.png'), dpi=200)