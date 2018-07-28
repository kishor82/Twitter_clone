from flask import Flask,render_template ,session ,request,redirect ,url_for ,flash
from flask_pymongo import PyMongo
import bcrypt 

app=Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_URI']= "mongodb://localhost:27017/twitterdb"
mongo = PyMongo(app)

@app.route('/')
def home():
	if 'username' in session:
		users = mongo.db.users
		user_data = users.find_one({'_id':session['username']})
		#store all data as dictionary 
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


@app.route('/profile')
def profile():
	return 'profile'

@app.route('/userlist')
def userlist():
	return 'userlist'

@app.route('/logout')
def logout():
	return 'logout'



if __name__=='__main__':
	app.run(debug =True)