from flask import request, jsonify
from models import db, User, Invite
from app import mails
import datetime, re

def create():
	message = ''
	user = request.form['user']
	email = request.form['email'].lower()
	password = request.form['password']
	new_user = create_user(user, email, password, True)
	
	if new_user:
		message = 'horay'		
	
	data = {
		'id' : new_user.id,
		'name' : new_user.name,
		'email' : email,
		'password' : new_user.password,
		'fb_userid' : new_user.fb_userid,
		'subscribed' : new_user.subscribed,
		'games_played' : new_user.games_played,
		'friends_invited' : new_user.friends_invited,
		'curr_coins' : new_user.curr_coins,
		'total_coins_earned' : new_user.total_coins_earned,
		'total_coins_purchased' : new_user.total_coins_purchased,
		'curr_bombs' : new_user.curr_bombs,
		'status' : 'success',
		'message' : message
	}
	
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def create_user(name, email, password, subscribed):
	user = User.query.filter_by(email=email).first()
	
	if not user:
		new_user = User(
					name=name, 
					email=email, 
					password=password, 
					subscribed=subscribed,
					curr_bombs=0,
					curr_coins=0,
					total_coins_earned=0,
					total_coins_purchased=0,
					games_played=0,
					friends_invited=0,
					fb_userid='',
					created_at=datetime.datetime.now())
		db.session.add(new_user)
	else:
		if not user.subscribed:
			user.email = email
			user.name = name
			user.password = password
			user.subscribed = subscribed
			if subscribed:
				invite = Invite.query.filter_by(email=email).first()
				invite.subscribed = datetime.datetime.now()
			
		new_user = user
	db.session.commit()
	return new_user

def update_bombs():
	user = User.query.filter_by(email=request.form['email']).first()
	if user:
		user.curr_bombs = request.form['curr_bombs']
		user.recent_activity = datetime.datetime.now()
		db.session.commit()
		
	status = 'success'
	data = {
		'user_id' : user.id,
		'status' : status
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def update_coins():
	user = User.query.filter_by(email=request.form['email']).first()
	if user:
		user.curr_coins = request.form['curr_coins']
		user.total_coins_earned = request.form['total_coins_earned']
		user.total_coins_purchased = request.form['total_coins_purchased']
		user.recent_activity = datetime.datetime.now()
		db.session.commit()
		
	status = 'success'
	data = {
		'user_id' : user.id,
		'status' : status
	}
	resp = jsonify(data)
	resp.status_code = 200
	return resp
	
def update_user_facebook(email, fb_user):
	user = User.query.filter_by(email=email).first()
	if user:
		user.fb_userid = fb_user
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
	email = email.lower()
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
				users.append({
					'id' : user.id,
					'name' : user.name,
					'email' : email,
					'password' : user.password,
					'fb_userid' : user.fb_userid,
					'subscribed' : user.subscribed,
					'games_played' : user.games_played,
					'friends_invited' : user.friends_invited,
					'curr_coins' : user.curr_coins,
					'total_coins_earned' : user.total_coins_earned,
					'total_coins_purchased' : user.total_coins_purchased,
					'curr_bombs' : user.curr_bombs
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
	new_email = request.form['new_email'].lower()
	new_phone = request.form['new_phone']
	
	invited_a_person(email)
	create_user(new_name, new_email, "", False)
	#mails.send_invite_email(new_email, new_name, name, email)
	new_user = User.query.filter_by(email=new_email).first()
	invite = Invite.query.filter_by(email=new_email).first()
	if not invite:
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