from flask import Blueprint, request
import json
import os
import logging

adp_bp = Blueprint('adp', __name__)
PATH_PREFIX='jsons'

log = logging.getLogger("main")

def get_json_file_content(file_path):
    current_dir = os.path.dirname(__file__)
    with open(f'{current_dir}/{file_path}', 'r') as file:
        return json.load(file)

@adp_bp.route('/hr/v2/workers')
def hr_workers():
    return get_json_file_content('jsons/workers.json')

@adp_bp.route('/hr/v2/workers/<id>')
def hr_workers_detail(id):
    return get_json_file_content(f'{PATH_PREFIX}/workers_detail.json')

@adp_bp.route('/payroll/v2/workers/<id>/pay-distributions')
def pay_distributions(id):
    return get_json_file_content(f'{PATH_PREFIX}/pay_dist.json')


@adp_bp.route('/payroll/v1/workers/<id>/pay-statements')
def pay_statement(id):
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/pay_statement.json')


@adp_bp.route('/payroll/v1/workers/<id>/pay-statements/<uuid>')
def pay_statement_detail(id, uuid):
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/pay_statement_detail.json')

@adp_bp.route('/core/v2/organizations')
def organizations():
    return get_json_file_content(f'{PATH_PREFIX}/organization.json')

@adp_bp.route('/payroll/v1/pay-data-input')
def pay_data_input():
    log.info(f"request headers: {request.headers}")
    return get_json_file_content(f'{PATH_PREFIX}/pay_data_input.json')


@adp_bp.route('/auth/oauth/v2/token', methods=['POST'])
def auth():
    log.info(f"request headers: {request.headers}")
    return {
            "access_token": "asdkjfçalkdfjçsldkjfaçkdjslf",
            "expires_in": 36000
        }
