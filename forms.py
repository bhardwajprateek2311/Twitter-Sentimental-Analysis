
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class login1(FlaskForm):

	user1=StringField('user')
	pass1=StringField('password')
	submit=SubmitField('submit')
	

class register1(FlaskForm):
	pass2=StringField('password')
	pass3=StringField('password')
	email=StringField('email')
	user=StringField('user')
	submit1=SubmitField('submit')

class tweet_f(FlaskForm):
	ck=StringField('user1')
	cs=StringField('user2')
	at=StringField('user3')
	ats=StringField('user4')
	submit2=SubmitField('submit')


	

'''class twitter_det(FlaskForm):
	consumer_key = StringField(' ')
    consumer_secret = StringField(' ')
    access_token = StringField(' ')
    access_token_secret = StringField(' ')
    submit=SubmitField('submit')

class face_det(FlasForm):
	face_key=SubmitField(' ')
	submit=SubmitField('submit')'''
