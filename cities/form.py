from flask_wtf import Form
from wtforms import validators, StringField

class NewCityForm(Form):
    name = StringField('City Name', [validators.Required()])
    open311_endpoint = StringField('Endpoint', [validators.Required()])
    open311_jurisdiction = StringField('Jurisdiction')
