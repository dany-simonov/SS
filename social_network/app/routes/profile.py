from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import db

bp = Blueprint('profile', __name__)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    current_user.username = request.form.get('username', current_user.username)
    current_user.avatar_url = request.form.get('avatar_url', current_user.avatar_url)
    current_user.interests = request.form.get('interests', current_user.interests)
    
    db.session.commit()
    return jsonify({'success': True})
