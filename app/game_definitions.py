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
	new_game_result = Result(
					input_phrase=request.form['input_phrase'], 
					user_id=request.form['user_id'],
					initiating=request.form['initiating'], 
					game_id=request.form['game_id'],
					accuracy=request.form['accuracy'],
					finished=request.form['finished'],
					wpm=request.form['wpm'],
					duration=request.form['duration'],
					created_at=datetime.datetime.now())
					
	if not new_game_result.initiating:
		if new_game_result.finished:
			game = Game.query.filter_by(id=new_game_result.game_id).first()
			game.active = False
		
	db.session.add(new_game_result)
	db.session.commit()
	
	data = {
		'id' : new_game_result.id,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def games_for_user():
	user = User.query.filter_by(id=request.args['id']).first()
	games = Game.query.filter_by(game_owner=user.id)
	
	userItems = []
	userItems.append({
					'id' : user.id,
					'subscribed' : user.subscribed,
					'games_played' : user.games_played,
					'friends_invited' : user.friends_invited,
					'curr_coins' : user.curr_coins,
					'total_coins_earned' : user.total_coins_earned,
					'total_coins_purchased' : user.total_coins_purchased
				})
	gameItems = []
	gameResultItems = []
	userIDtracking = []
	for game in games:
		gameItems.append({
			'id' : game.id,
			'phrase_id' : game.phrase_id,
			'prev_game_id' : game.prev_game_id,
			'consec_game_count' : game.consec_game_count,
			'active' : game.active,
			'responded_to' : game.responded_to,
			'game_owner' : game.game_owner,
		})
		gameResults = Result.query.filter_by(game_id=game.id)
		for gameResult in gameResults:
			user = User.query.filter_by(id=gameResult.user_id).first()
			if not user.id in userIDtracking:
				userIDtracking.append(user.id)
				userItems.append({
						'id' : user.id,
						'subscribed' : user.subscribed,
						'games_played' : user.games_played,
						'friends_invited' : user.friends_invited,
						'curr_coins' : user.curr_coins,
						'total_coins_earned' : user.total_coins_earned,
						'total_coins_purchased' : user.total_coins_purchased
					})
			gameResultItems.append({
					'id' : gameResult.id,
					'input_phrase' : gameResult.input_phrase,
					'finished' : gameResult.finished,
					'initiating' : gameResult.initiating,
					'game_id' : gameResult.game_id
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