from flask import request, jsonify
from models import db, User, Invite
from app import mails
import datetime, re

def create():
	message = ''
	user = request.form['user']
	email = request.form['email']
	password = request.form['password']
	new_user = create_user(user, email, password, True)
	
	if new_user:
		message = 'horay'		
	
	data = {
		'id' : new_user.id,
		'status' : 'success',
		'message' : message
	}
	
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def create_user(name, email, password, subscribed):
	new_user = User(
					name=name, 
					email=email, 
					password=password, 
					subscribed=subscribed,
					created_at=datetime.datetime.now())
	db.session.add(new_user)
	db.session.commit()
	return new_user

def update_user_facebook(name, email, fb_user):
	user = User.query.filter_by(email=email).first()
	if user:
		user.fb_userid = fb_user
		user.recent_activity = datetime.datetime.now()
		db.session.commit()

def update_user_coins(email, new_coins):
	user = User.query.filter_by(email=email).first()
	if user:
		if user.curr_coins == None:
			user.curr_coins = user.curr_coins + new_coins
		else:
			user.curr_coins = new_coins
			
		if user.total_coins_earned == None:
			user.total_coins_earned = user.total_coins_earned + new_coins
		else:
			user.total_coins_earned = new_coins
			
		user.recent_activity = datetime.datetime.now()
		
		db.session.commit()

def invited_a_person(email):
	user = User.query.filter_by(email=email).first()
	if user:
		if user.friends_invited:
			user.friends_invited = user.friends_invited + 1
		else:
			user.friends_invited = 1
		user.recent_activity = datetime.datetime.now()
		db.session.commit()
		
def login(email, password):
	status = ''
	message = ''
	users = []
	if len(email) == 0:
		status = 'failure'
		message = 'please enter an email address'
	else:
		user = User.query.filter_by(email=email).first()
		if user:
			if ((user.password == password) & user.subscribed):
				status = 'success'
				message = 'thanks for visiting'
				user.append({
					'id' : user.id,
					'name' : user.name,
					'subscribed' : user.subscribed,
					'games_played' : user.games_played,
					'friends_invited' : user.friends_invited,
					'curr_coins' : user.curr_coins,
					'total_coins_earned' : user.total_coins_earned,
					'total_coins_purchased' : user.total_coins_purchased
				})
			else:
				status = 'failure'
				message = 'password mismatch'
		
	data = {
		'status' : status,
		'users' : users,
		'message' : message
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp

def invite():
	email = request.form['email']
	name = request.form['name']
	new_name = request.form['new_name']
	new_email = request.form['new_email']
	new_phone = request.form['new_phone']
	
	invited_a_person(email)
	create_user(new_name, new_email, "", False)
	#mails.send_invite_email(new_email, new_name, name, email)
	new_user = User.query.filter_by(email=new_email).first()
	invite = Invite(
				user_id=new_user.id, 
				name=request.form['new_name'],
				phone=request.form['new_phone'],
				email=request.form['new_email'],
				created_at=datetime.datetime.now())
	db.session.add(invite)
	db.session.commit()
	
	data = {
		'user_id' : new_user.id,
		'invite_id' : invite.id,
		'status' : 'success'
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp