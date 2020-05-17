from flask import Blueprint, render_template

from dinnerat7 import find_dating_events

bp = Blueprint('api_web', __name__, url_prefix='/api/web')


@bp.route('/')
def api_default():
    dating_events = find_dating_events()
    return render_template('index.html', events=dating_events)