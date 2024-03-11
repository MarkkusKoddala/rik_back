from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import update, insert, func
from sqlalchemy.orm import aliased

from models import db, LegalPerson, companies_legal_person_shareholders, companies_natural_person_shareholders, Company, \
    NaturalPerson

bp = Blueprint('main', __name__)

@bp.route('/search', methods=['GET'])
def get_companies():
    company_name = request.args.get('companyName', '')
    register_code = request.args.get('companyCode', '')
    shareholder_name = request.args.get('shareholderName', '')
    shareholder_code = request.args.get('shareholderCode', '')

    query = Company.query

    if company_name:
        query = query.filter(Company.name.ilike(f'%{company_name}%'))
    if register_code:
        query = query.filter(Company.register_code.ilike(f'%{register_code}%'))

    if shareholder_name or shareholder_code:
        query = query.join(Company.legal_shareholders).join(Company.natural_shareholders)

        if shareholder_name:
            shareholder_name_filter = (
                    LegalPerson.name.ilike(f'%{shareholder_name}%') |
                    NaturalPerson.first_name.ilike(f'%{shareholder_name}%') |
                    NaturalPerson.last_name.ilike(f'%{shareholder_name}%')
            )
            query = query.filter(shareholder_name_filter)

        if shareholder_code:
            shareholder_code_filter = (
                    LegalPerson.register_code.ilike(f'%{shareholder_code}%') |
                    NaturalPerson.identification_code.ilike(f'%{shareholder_code}%')
            )
            query = query.filter(shareholder_code_filter)

        query = query.distinct()

    results = query.all()
    return jsonify([{'name': company.name, 'register_code': company.register_code} for company in results])


@bp.route('/company_data', methods=['GET'])
def get_company_data():
    register_code = request.args.get('registerCode', '')
    company = Company.query.filter_by(register_code=register_code).first()

    if not company:
        return jsonify({"error": "Company not found."}), 404

    np_alias = aliased(NaturalPerson)
    lp_alias = aliased(LegalPerson)

    natural_persons_query = db.session.query(
        (np_alias.first_name + ' ' + np_alias.last_name).label('name'),
        np_alias.identification_code.label('identification_code'),
        companies_natural_person_shareholders.c.share_size,
        companies_natural_person_shareholders.c.is_founder
    ).join(
        companies_natural_person_shareholders,
        np_alias.identification_code == companies_natural_person_shareholders.c.natural_person_identification_code
    ).filter(
        companies_natural_person_shareholders.c.company_register_code == company.register_code
    )

    legal_persons_query = db.session.query(
        lp_alias.name.label('name'),
        lp_alias.register_code.label("identification_code"),
        companies_legal_person_shareholders.c.share_size,
        companies_legal_person_shareholders.c.is_founder
    ).join(
        companies_legal_person_shareholders,
        lp_alias.register_code == companies_legal_person_shareholders.c.legal_person_register_code
    ).filter(
        companies_legal_person_shareholders.c.company_register_code == company.register_code
    )

    combined_query = natural_persons_query.union(legal_persons_query)
    shareholders = combined_query.all()

    company_data = {
        "name": company.name,
        "register_code": company.register_code,
        "formation_date": company.registered_on.isoformat(),
        "total_capital": company.total_capital,
        "shareholders": [{
            "name": shareholder.name,
            "identification_code": shareholder.identification_code,
            "share_size": shareholder.share_size,
            "is_founder": shareholder.is_founder
        } for shareholder in shareholders]
    }

    return jsonify(company_data), 200


@bp.route('/persons', methods=['GET'])
def get_persons():
    np_alias = aliased(NaturalPerson)
    lp_alias = aliased(LegalPerson)

    natural_persons = db.session.query(
        (np_alias.first_name + ' ' + np_alias.last_name).label('name'),
        np_alias.identification_code.label("identification_code")
    )

    legal_persons = db.session.query(
        lp_alias.name.label("name"),
        lp_alias.register_code.label("identification_code")
    )

    combined_query = natural_persons.union(legal_persons)

    persons = combined_query.all()

    persons_list = [{"name": person.name, "identification_code": person.identification_code} for person in persons]

    return jsonify(persons_list), 200


@bp.route('/add_company', methods=['POST'])
def add_company():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    establishment_date = datetime.fromisoformat(json_data['establishmentDate'].rstrip('Z'))  # Remove 'Z' if present

    if Company.query.filter_by(register_code=json_data['registerCode']).first():
        return jsonify({'message': 'Ettevõtte samasuguse registrikoodiga juba eksisteerib'}), 400

    new_company = Company(
        name=json_data['companyName'],
        register_code=json_data['registerCode'],
        registered_on=establishment_date.date(),
        total_capital=json_data['totalCapital']
    )

    db.session.add(new_company)

    for shareholder_data in json_data['shareholders']:
        shareholder_code = shareholder_data['identification_code']
        legal_person = LegalPerson.query.filter_by(register_code=shareholder_code).first()
        natural_person = NaturalPerson.query.filter_by(identification_code=shareholder_code).first()

        if legal_person:
            db.session.execute(companies_legal_person_shareholders.insert().values(
                company_register_code=json_data['registerCode'],
                legal_person_register_code=shareholder_code,
                share_size=shareholder_data["shareSize"],
                is_founder=shareholder_data["isFounder"]
            ))
        elif natural_person:
            db.session.execute(companies_natural_person_shareholders.insert().values(
                company_register_code=json_data['registerCode'],
                natural_person_identification_code=shareholder_code,
                share_size=shareholder_data["shareSize"],
                is_founder=shareholder_data["isFounder"]
            ))

        else:
            db.session.rollback()
            return jsonify({'message': f'Shareholder with code {shareholder_code} not found'}), 404

    try:
        db.session.commit()
        return jsonify({'message': 'Company and shareholders added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add company and shareholders', 'error': str(e)}), 500


@bp.route('/edit_shareholders', methods=['POST'])
def edit_shareholders():
    data = request.get_json()

    register_code = data['registerCode']
    shareholders_data = data['shareholders']

    company = Company.query.filter_by(register_code=register_code).first()

    for shareholder in shareholders_data:

        share_size = shareholder['share_size']
        identification_code = shareholder['identification_code']

        # Determine if shareholder is legal or natural
        legal_person = LegalPerson.query.filter_by(register_code=identification_code).first()
        natural_person = NaturalPerson.query.filter_by(identification_code=identification_code).first()

        if legal_person:
            table = companies_legal_person_shareholders
            person_id_col = 'legal_person_register_code'
        elif natural_person:
            table = companies_natural_person_shareholders
            person_id_col = 'natural_person_identification_code'
        else:
            continue

        existing_entry = db.session.query(table).filter(
            table.c.company_register_code == register_code,
            getattr(table.c, person_id_col) == identification_code
        ).first()

        if existing_entry:
            db.session.execute(update(table).values(
                share_size=share_size
            ).where(
                table.c.company_register_code == register_code,
                getattr(table.c, person_id_col) == identification_code
            ))
        else:
            db.session.execute(insert(table).values(
                company_register_code=register_code,
                **{person_id_col: identification_code},
                share_size=share_size,
                is_founder=False
            ))

    total_share_size = 0
    total_share_size += db.session.query(func.sum(companies_legal_person_shareholders.c.share_size)).filter(
        companies_legal_person_shareholders.c.company_register_code == register_code).scalar() or 0
    total_share_size += db.session.query(func.sum(companies_natural_person_shareholders.c.share_size)).filter(
        companies_natural_person_shareholders.c.company_register_code == register_code).scalar() or 0

    company.total_capital = total_share_size

    try:
        db.session.commit()
        return jsonify({'message': 'Shareholders edited successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': str(e), 'message': 'Failed to edit shareholders'}), 500
