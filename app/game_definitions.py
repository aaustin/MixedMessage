from flask import request, jsonify
from models import db, User, Invite, Game, Result
import datetime

def create_game():
	new_game = Game(
					phrase_id=request.form['phrase_id'], 
					game_owner=request.form['user_id'],
					prev_game_id=request.form['prev_game_id'], 
					consec_game_count=request.form['consec_game_count'], 
					active=True,
					created_at=datetime.datetime.now())
	db.session.add(new_game)
	db.session.commit()
	
	data = {
		'id' : new_game.id,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def create_game_result():
	result = Result.query.filter_by(id=request.form['id']).first()

	if not result:
		if request.form['finished'] == '0':
			result = Result(
					input_phrase='', 
					user_id=request.form['user_id'],
					initiating=False, 
					game_id=request.form['game_id'],
					accuracy=0,
					finished=False,
					wpm=0,
					duration=0,
					created_at=datetime.datetime.now())
		else:
			result = Result(
					input_phrase=request.form['input_phrase'], 
					user_id=request.form['user_id'],
					initiating=True, 
					game_id=request.form['game_id'],
					accuracy=request.form['accuracy'],
					finished=True,
					wpm=request.form['wpm'],
					duration=request.form['duration'],
					created_at=datetime.datetime.now())
					
			increment_games_played(request.form['user_id'])
			
		db.session.add(result)
	else:
		result.finished = True
		result.input_phrase = request.form['input_phrase']
		result.accuracy=request.form['accuracy']
		result.wpm=request.form['wpm']
		result.duration=request.form['duration']
		
					
	if not result.initiating:
		if result.finished:
			increment_games_played(request.form['user_id'])
			game = Game.query.filter_by(id=result.game_id).first()
			game.active = False
			game.responded_to = datetime.datetime.now()
	
	db.session.commit()
	
	data = {
		'id' : result.id,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp

def increment_games_played(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user:
		if user.games_played:
			user.games_played = user.games_played + 1
		else:
			user.games_played = 1
	
def games_for_user():
	gameItems = []
	gameResultItems = []
	userItems = []
	
	userIDtracking = []
	gameIDtracking = []
	
	user = User.query.filter_by(id=request.args.get('id')).first()
	gameResults = Result.query.filter_by(user_id=user.id)
	for gameResult in gameResults:
		if not gameResult.game_id in gameIDtracking:
			gameIDtracking.append(gameResult.game_id)
		
	for gameID in gameIDtracking:
		game = Game.query.filter_by(id=gameID).first()
		gameItems.append({
			'id' : game.id,
			'phrase_id' : game.phrase_id,
			'prev_game_id' : game.prev_game_id,
			'consec_game_count' : game.consec_game_count,
			'active' : game.active,
			'game_owner' : game.game_owner,
			'created_at' : game.created_at.strftime('%m/%d/%Y')
		})
		gameResults = Result.query.filter_by(game_id=game.id)
		for gameResult in gameResults:
			userN = User.query.filter_by(id=gameResult.user_id).first()
			if not userN.id in userIDtracking:
				userIDtracking.append(userN.id)
				userItems.append({
						'id' : userN.id,
						'name' : userN.name,
						'email' : userN.email,
						'fb_userid' : userN.fb_userid,
						'subscribed' : userN.subscribed,
						'games_played' : userN.games_played,
						'friends_invited' : userN.friends_invited,
						'curr_coins' : userN.curr_coins,
						'total_coins_earned' : userN.total_coins_earned,
						'total_coins_purchased' : userN.total_coins_purchased,
						'curr_bombs' : user.curr_bombs,
						'created_at' : userN.created_at.strftime('%m/%d/%Y')
					})
			gameResultItems.append({
					'id' : gameResult.id,
					'wpm' : gameResult.wpm,
					'accuracy' : gameResult.accuracy,
					'duration' : gameResult.duration,
					'user_id' : gameResult.user_id,
					'input_phrase' : gameResult.input_phrase,
					'finished' : gameResult.finished,
					'initiating' : gameResult.initiating,
					'game_id' : gameResult.game_id,
					'created_at' : gameResult.created_at.strftime('%m/%d/%Y')
			})
			
	data = {
		'gameItems' : gameItems,
		'gameResultItems' : gameResultItems,
		'userItems' : userItems,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp