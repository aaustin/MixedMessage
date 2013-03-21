from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(64), index = True, unique = True)
	phone = db.Column(db.String(64))
	password = db.Column(db.String(64))
	subscribed = db.Column(db.Boolean)
	fb_userid = db.Column(db.String(64), index = True)
	curr_coins = db.Column(db.Integer)
	curr_bombs = db.Column(db.Integer)
	total_coins_earned = db.Column(db.Integer)
	total_coins_purchased = db.Column(db.Integer)
	games_played = db.Column(db.Integer)
	friends_invited = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	recent_activity = db.Column(db.DateTime)	
	
	def __repr__(self):
		return '<User %r>' % (self.email)

class Invite(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(db.String(64))
	phone = db.Column(db.String(64))
	email = db.Column(db.String(64), index = True)
	created_at = db.Column(db.DateTime)
	subscribed = db.Column(db.DateTime)	
	
	def __repr__(self):
		return '<Invite %r>' % (self.email)
		
class Result(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	input_phrase = db.Column(db.String(255))
	accuracy = db.Column(db.Float)
	wpm = db.Column(db.Float)
	duration = db.Column(db.Float)
	initiating = db.Column(db.Boolean)
	finished = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))	
	game_id = db.Column(db.Integer, db.ForeignKey('game.id')) 
	
	def __repr__(self):
		return '<Result %r>' % (self.id)

class Game(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	phrase_id = db.Column(db.Integer)
	prev_game_id = db.Column(db.Integer)
	consec_game_count = db.Column(db.Integer)
	active = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime)
	responded_to = db.Column(db.DateTime)
	game_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Game %r>' % (self.id)

		
class Phrase(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	type = db.Column(db.String(64))
	phrase = db.Column(db.String(255))
	priority = db.Column(db.Integer)
	active = db.Column(db.Boolean)
	
	def __repr__(self):
		return '<Phrase %r>' % (self.id)