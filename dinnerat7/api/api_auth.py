from flask import Blueprint, jsonify, request
import pprint

from dinnerat7.database import register_user

bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@bp.route('/', methods=['POST'])
def api_default():
    content = request.json
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(content)
    user = content.get('user', {})
    email, display_name = user.get('email'), user.get('displayName')
    user = register_user(email, display_name)
    return jsonify(user=user.as_dict())
