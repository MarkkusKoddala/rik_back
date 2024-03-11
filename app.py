from flask import Flask
import logging
from datetime import date
from database_setup import seed_data
from models import db, LegalPerson, Company, companies_legal_person_shareholders
from routes import bp
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(bp, url_prefix='/api')


with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    app.run(debug=True)
