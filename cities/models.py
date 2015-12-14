from open311_comparison import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    open311_endpoint = db.Column(db.String(150), unique=True)
    open311_jurisdiction = db.Column(db.String(150), unique=True)
    is_active = db.Column(db.Boolean)

    def __init__(self, city_name, city_open311_api_endpoint, city_open311_jurisdiction='', is_active=True):
        self.name = city_name
        self.open311_endpoint = city_open311_api_endpoint
        self.open311_jurisdiction = city_open311_jurisdiction
        self.is_active = is_active
    
    def __repr__(self):
        return '<City %r>' % self.name

ViewTypes = ('heatmap','days','hours', 'hour_heatmap')