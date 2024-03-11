from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Integer, Table, Column, String, ForeignKey, UniqueConstraint, Boolean, Date
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Ensure this is after initializing db but before defining models that use it
companies_legal_person_shareholders = db.Table('companies_legal_person_shareholders',
                                               db.Column('company_register_code', db.String, db.ForeignKey('company.register_code')),
                                               db.Column('legal_person_register_code', db.String, db.ForeignKey('legal_person.register_code')),
                                               db.Column('share_size', db.Integer, CheckConstraint('share_size >= 1'), nullable=False),
                                               db.Column('is_founder', db.Boolean, nullable=False),
)

companies_natural_person_shareholders = db.Table('companies_natural_person_shareholders',
                                                 db.Column('company_register_code',db.String, db.ForeignKey('company.register_code')),
                                                 db.Column('natural_person_identification_code',db.String, db.ForeignKey('natural_person.identification_code')),
                                                 db.Column('share_size', db.Integer,
                                                           CheckConstraint('share_size >= 1'), nullable=False),
                                                 db.Column('is_founder', db.Boolean, nullable=False)
                                                 )


class LegalPerson(db.Model):
    register_code = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    companies = db.relationship('Company', secondary=companies_legal_person_shareholders,
                                back_populates='legal_shareholders')


class Company(db.Model):
    register_code = db.Column(db.String(7), CheckConstraint('LENGTH(register_code) = 7'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.Date, CheckConstraint('registered_on <= CURRENT_DATE'), nullable=False)
    total_capital = db.Column(Integer, CheckConstraint('total_capital >= 2500'), nullable=False)
    legal_shareholders = relationship('LegalPerson', secondary=companies_legal_person_shareholders,
                                      back_populates='companies')
    natural_shareholders = relationship('NaturalPerson', secondary=companies_natural_person_shareholders,
                                        back_populates='companies')


class NaturalPerson(db.Model):
    identification_code = db.Column(db.String(11), primary_key=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    companies = relationship('Company', secondary=companies_natural_person_shareholders,
                             back_populates='natural_shareholders')
