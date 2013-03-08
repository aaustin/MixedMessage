from flask import request
from app import user_definitions, phrase_definitions, game_definitions
from app import app

@app.route('/')
@app.route('/index')
def index():   
	return ""

@app.route('/users/create', methods=['POST'])
def create_user_view():   
	return user_definitions.create()	

@app.route('/users/invite', methods=['POST'])
def invite_user_view():   
	return user_definitions.invite()

@app.route('/users/login')
def login_user_view():
	return user_definitions.login(request.args['email'], request.args['password'])	
	
@app.route('/phrases/all')
def grab_all_phrases():
	return phrase_definitions.all_phrases()	
	
@app.route('/games/create', methods=['POST'])
def create_game_view():
	return game_definitions.create_game()	

@app.route('/games/result/create', methods=['POST'])
def create_game_result_view():
	return game_definitions.create_game_result()	

@app.route('/users/games')
def grab_games_for_user():
	return game_definitions.games_for_user()