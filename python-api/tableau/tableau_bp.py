from flask import Blueprint, request
import json
import os
import logging

tableau_bp = Blueprint('tableau', __name__)
PATH_PREFIX='jsons'

log = logging.getLogger("main")

def get_json_file_content(file_path):
    current_dir = os.path.dirname(__file__)
    with open(f'{current_dir}/{file_path}', 'r') as file:
        return json.load(file)

@tableau_bp.route('/api/3.4/auth/signin', methods=["POST"])
@tableau_bp.route('/api/3.21/auth/signin', methods=["POST"])
def tableu_auth():
    return {
        "credentials": {
            "token": "tableau_fake_token"
        }
    }

@tableau_bp.route('/api/3.21/sessions/current')
def session():
    return {
        "session": {
            "site": {
                "id": 123
            }
        }
    }

@tableau_bp.route('/api/3.21/sites/<id>/projects')
def projects(id):
    return get_json_file_content(f'{PATH_PREFIX}/projects')


@tableau_bp.route('/api/3.21/sites/{{ extractions.site_id }}/workbooks')
def workbooks(id):
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/workbooks')


@tableau_bp.route('/payroll/v1/workers/<id>/pay-statements/<uuid>')
def pay_statement_detail(id, uuid):
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/pay_statement_detail.json')

@tableau_bp.route('/core/v2/organizations')
def organizations():
    return get_json_file_content(f'{PATH_PREFIX}/organization.json')

@tableau_bp.route('/payroll/v1/pay-data-input')
def pay_data_input():
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/pay_data_input.json')


@tableau_bp.route('/auth/oauth/v2/token', methods=['POST'])
def auth():
    log.info(f"request headers: {request.headers}")
    return {
            "access_token": "asdkjfçalkdfjçsldkjfaçkdjslf",
            "expires_in": 36000
        }
