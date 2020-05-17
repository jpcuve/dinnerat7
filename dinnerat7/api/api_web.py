from flask import Blueprint, render_template, current_app

from dinnerat7 import find_dating_events

bp = Blueprint('api_web', __name__, url_prefix='/api/web')


@bp.route('/')
def api_default():
    dating_events = find_dating_events()
    return render_template('index.html', events=dating_events)


@bp.route('/auth')
def api_auth():
    return render_template(
        'auth.html',
        firebase_api_key=current_app.config['FIREBASE_API_KEY'],
        firebase_auth_domain=current_app.config['FIREBASE_AUTH_DOMAIN'],
        firebase_database_url=current_app.config['FIREBASE_DATABASE_URL'],
        firebase_project_id=current_app.config['FIREBASE_PROJECT_ID'],
        firebase_storage_bucket=current_app.config['FIREBASE_STORAGE_BUCKET'],
        firebase_messaging_sender_id=current_app.config['FIREBASE_MESSAGING_SENDER_ID'],
        firebase_app_id=current_app.config['FIREBASE_APP_ID'],
        firebase_measurement_id=current_app.config['FIREBASE_MEASUREMENT_ID']
    )


@bp.route('/privacy-policy')
def api_privacy_policy():
    return render_template('privacy-policy.html')


@bp.route('/terms-of-service')
def api_terms_of_service():
    return render_template('terms-of-service.html')
