from flask import Blueprint, request, jsonify
from app.models import JournalEntry
from app import db

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    try:
        entry = JournalEntry(
            title=data['title'],
            content=data['content'],
            mood=data.get('mood'),
            tags=data.get('tags')
        )
        entry.save()
        return jsonify(entry.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@journal_bp.route('/entries', methods=['GET'])
def get_entries():
    # Support for filtering and searching
    mood = request.args.get('mood')
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    if mood:
        entries = JournalEntry.get_by_mood(mood)
    elif tag:
        entries = JournalEntry.get_by_tag(tag)
    elif search:
        entries = JournalEntry.search_by_title(search)
    else:
        entries = JournalEntry.get_all()
    
    return jsonify([entry.to_dict() for entry in entries])

@journal_bp.route('/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = JournalEntry.get_by_id(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    return jsonify(entry.to_dict())

@journal_bp.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = JournalEntry.get_by_id(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'title' in data:
            entry.title = data['title']
        if 'content' in data:
            entry.content = data['content']
        if 'mood' in data:
            entry.mood = data['mood']
        if 'tags' in data:
            entry.tags = data['tags']
        
        entry.save()
        return jsonify(entry.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@journal_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = JournalEntry.get_by_id(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    entry.delete()
    return '', 204

@journal_bp.route('/entries/<int:entry_id>/tags', methods=['POST'])
def add_tag(entry_id):
    entry = JournalEntry.get_by_id(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    data = request.get_json()
    if not data or 'tag' not in data:
        return jsonify({'error': 'Tag is required'}), 400
    
    entry.add_tag(data['tag'])
    return jsonify(entry.to_dict())

@journal_bp.route('/entries/<int:entry_id>/tags/<tag>', methods=['DELETE'])
def remove_tag(entry_id, tag):
    entry = JournalEntry.get_by_id(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    entry.remove_tag(tag)
    return jsonify(entry.to_dict()) 