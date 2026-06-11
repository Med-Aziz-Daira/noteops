from flask import Blueprint, jsonify, request
from app import db
from app.models import Note

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notes]), 200


@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'title and content are required'}), 400
    note = Note(title=data['title'], content=data['content'])
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        return jsonify({'error': 'not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200
