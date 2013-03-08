from flask import request, jsonify
from models import db, User, Phrase

def all_phrases():
	phrases = Phrase.query.all()
	
	phraseItems = []
	for phrase in phrases:
		if phrase.active:
			phraseItems.append({
				'id' : phrase.id,
				'type' : phrase.type,
				'phrase' : phrase.phrase,
				'priority' : phrase.priority,
				'active' : phrase.active
			})
	data = {
		'items' : phraseItems,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp