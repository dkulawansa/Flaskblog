import logging
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5eff0e854b7a55a95084e52fa4a1ae43'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db= SQLAlchemy(app)

posts = [{'author': 'Corey Schafer',
		  'title': 'Blog Post 1',
          'content': 'First post content',
		  'date_posted': 'April 20, 2018'
		  },
		 {'author': 'Jane Doe',
		  'title': 'Blog Post 2',
		  'content': 'Second post content',
		  'date_posted': 'April 21, 2019'
		  }
		 ]
@app.route('/')
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
	    flash(f'Account created for {form.username.data}!', 'success')
	    return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
		    flash('You have been logged in!', 'success')
		    return redirect(url_for('home'))
		else:
			flash('Log in Unsuccessful. Please check username and password', 'danger')
			return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500



if __name__ == "__main__":
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)

