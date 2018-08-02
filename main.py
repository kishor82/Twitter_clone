from flask import Flask,render_template ,session ,request,redirect ,url_for ,flash ,g
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt

app=Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_URI']= "mongodb://localhost:27017/twitterdb"
mongo = PyMongo(app)

@app.route('/')
def home():
	if 'username' in session:
		users = mongo.db.users
		user_data = users.find_one({'name':session['username']})
		#store all data as dictionary 
		#all_user= users.find()
		#records = dict((record['_id'],record) for record in all_user)
		return render_template('home.html', session = session)

	return render_template('login.html') 


@app.route('/login',methods=['POST'])
def login():
	error =None
	users = mongo.db.users
	login_user = users.find_one({'name':request.form['username']})

	if login_user:
		if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
			session['username'] = request.form['username']
			return redirect(url_for('home'))
		else:
				error = 'Invalid Credentials'
	else:
		error = 'Invalid Credentials	'


	return render_template('login.html',error=error)


@app.route('/register', methods=['POST','GET'])
def register():
	if request.method == 'POST':
		users = mongo.db.users
		existing_user = users.find_one({'name': request.form['username']})

		if existing_user is None:
			hashpass  = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
			users.insert({'name':request.form['username'],'password':hashpass})
			session['username'] = request.form['username']
			return redirect(url_for('home'))
		else:
			error = 'That username already exist!'

		return render_template('register.html' , error = error)

	return render_template('register.html')


@app.route('/profile/<id>')
def profile(id):
	users =mongo.db.users
	user_data = users.find_one({'name':session['username']})
	#it take about 4 hous to solve this very confusing though!!
	profile_id=request.args.get('id')
	profileData = users.find_one({'_id':ObjectId(profile_id)})

	tweet =mongo.db.tweets

	result = tweet.find()
	records = dict((record['_id'],record) for record in result)

	return render_template('home.html',records =records)


@app.route('/userlist')
def userlist():
	return render_template('under_construction.html')

@app.route('/logout')
def logout():
	return render_template('under_construction.html')
	 
@app.route('/create_tweet',methods =['POST','GET'])
def create_tweet():
	if request.method == 'POST':
		users = mongo.db.users
		user_id = session['username']
		user_data = users.find_one({'name':session['username']})
		body = request.form['body']
		date = datetime.now().strftime('%d-%m-%y %H:%M')

		tweet =mongo.db.tweets

		tweets = tweet.insert_one({
			'authorID':user_id,
			'authorName':user_data['name'],
			'body':body,
			'created':date
			})

		return redirect(url_for('home'))

if __name__=='__main__':
	app.run(debug =True)