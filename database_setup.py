from datetime import date
from models import db, LegalPerson, Company, companies_legal_person_shareholders, NaturalPerson, companies_natural_person_shareholders



def seed_legal_person():
    initial_legal_person = [
        {'name': 'Kalle Advokaadibüroo', 'register_code': '123456789'},
        {'name': 'Tarkade Koda ', 'register_code': '987654321'},
    ]

    for user_data in initial_legal_person:
        existing_user = LegalPerson.query.filter_by(register_code=user_data['register_code']).first()
        if not existing_user:
            new_user = LegalPerson(**user_data)
            db.session.add(new_user)
    db.session.commit()

def seed_natural_person():
    initial_natural_person = [
        {'first_name': 'Mari', 'last_name': 'Maasikas', 'identification_code': '47802039812'},
        {'first_name': 'Lendav', 'last_name': 'Orav', 'identification_code': '50102036112'},
    ]

    for person_data in initial_natural_person:
        existing_person = NaturalPerson.query.filter_by(identification_code=person_data['identification_code']).first()
        if not existing_person:
            new_person = NaturalPerson(**person_data)
            db.session.add(new_person)
    db.session.commit()

def seed_companies():
    initial_companies = [
        {'name': 'Tech Innovations OÜ', 'register_code': '1111111', 'registered_on': date(2020, 1, 1), 'total_capital': 8000},
        {'name': 'Green Energy AS', 'register_code': '2222222', 'registered_on': date(2021, 6, 15), 'total_capital': 12500},
        {'name': 'Tarkuse Tera OÜ', 'register_code': '3333333', 'registered_on': date(2012, 2, 21), 'total_capital': 5000},
        {'name': 'Sai ja Leib OÜ', 'register_code': '1234567', 'registered_on': date(2012, 2, 21), 'total_capital': 5500},
    ]

    for company_data in initial_companies:
        existing_company = Company.query.filter_by(register_code=company_data['register_code']).first()
        if not existing_company:
            new_company = Company(**company_data)
            db.session.add(new_company)
    db.session.commit()

def seed_company_shareholders_legal():
    company_shareholders_data = [
        {'legal_person_register_code': '123456789', 'company_register_code': '1111111', 'share_size': 5000, 'is_founder': True},
        {'legal_person_register_code': '987654321', 'company_register_code': '2222222', 'share_size': 7500, 'is_founder': True},
        {'legal_person_register_code': '123456789', 'company_register_code': '3333333', 'share_size': 2000,
         'is_founder': True},
        {'legal_person_register_code': '123456789', 'company_register_code': '1234567', 'share_size': 1000,
         'is_founder': True},


    ]

    for data in company_shareholders_data:
        legal_person_exists = db.session.query(
            db.exists().where(LegalPerson.register_code == data['legal_person_register_code'])
        ).scalar()
        company_exists = db.session.query(
            db.exists().where(Company.register_code == data['company_register_code'])
        ).scalar()

        if legal_person_exists and company_exists:
            existing_association = db.session.query(
                db.exists().where(db.and_(
                    companies_legal_person_shareholders.c.company_register_code == data['company_register_code'],
                    companies_legal_person_shareholders.c.legal_person_register_code == data['legal_person_register_code']
                ))
            ).scalar()

            if not existing_association:
                db.session.execute(
                    companies_legal_person_shareholders.insert().values(
                        company_register_code=data['company_register_code'],
                        legal_person_register_code=data['legal_person_register_code'],
                        share_size=data['share_size'],
                        is_founder=data['is_founder']
                    )
                )
                db.session.commit()



def seed_company_shareholders_natural():
    company_shareholders_natural = [
        {'natural_person_identification_code': '47802039812', 'company_register_code': '2222222', 'share_size': 5000,
         'is_founder': True},
        {'natural_person_identification_code': '50102036112', 'company_register_code': '1111111', 'share_size': 3000,
         'is_founder': True},
        {'natural_person_identification_code': '47802039812', 'company_register_code': '1234567', 'share_size': 2500,
         'is_founder': True},
        {'natural_person_identification_code': '50102036112', 'company_register_code': '1234567', 'share_size': 2000,
         'is_founder': True}
    ]

    for data in company_shareholders_natural:
        natural_person_exists = db.session.query(
            db.exists().where(NaturalPerson.identification_code == data['natural_person_identification_code'])
        ).scalar()
        company_exists = db.session.query(
            db.exists().where(Company.register_code == data['company_register_code'])
        ).scalar()

        if natural_person_exists and company_exists:
            existing_association = db.session.query(
                db.exists().where(db.and_(
                    companies_natural_person_shareholders.c.company_register_code == data['company_register_code'],
                    companies_natural_person_shareholders.c.natural_person_identification_code == data[
                        'natural_person_identification_code']
                ))
            ).scalar()

            if not existing_association:
                db.session.execute(
                    companies_natural_person_shareholders.insert().values(
                        company_register_code=data['company_register_code'],
                        natural_person_identification_code=data['natural_person_identification_code'],
                        share_size=data['share_size'],
                        is_founder=data['is_founder']
                    )
                )
                db.session.commit()



def seed_data():
    seed_companies()
    seed_legal_person()
    seed_company_shareholders_legal()
    seed_company_shareholders_natural()
    seed_natural_person()