from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Message, User, db

bp = Blueprint('chat', __name__)

@bp.route('/chat/<int:receiver_id>')
@login_required
def chat(receiver_id):
    receiver = User.query.get_or_404(receiver_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & 
         (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & 
         (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()
    return render_template('chat.html', receiver=receiver, messages=messages)

@bp.route('/send_message/<int:receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    content = request.json.get('message')
    if not content:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })
