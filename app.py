import dataclasses
import logging

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
ch.setFormatter(formatter)

log.addHandler(ch)

log.info("App starting...")

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

@dataclass
class User(db.Model):

    __tablename__ = "users"

    _id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    _username: Mapped[str] = db.Column(db.String(32), unique=True, nullable=False)
    _password: Mapped[str] = db.Column(db.String(16), nullable=False)

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, v: str):
        self._username = v

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, v: str):
        self._password = v

db.init_app(app)
with app.app_context():
    db.create_all()

# with app.app_context():
#     user = User()
#     user.username = "User"
#     user.password = "123"
#     db.session.add(user)
#     db.session.commit()
#     admin = User()
#     admin.username = "Admin"
#     admin.password = "123"
#     db.session.add(admin)
#     db.session.commit()
# migrate = Migrate(app, db)

# Set the secret key to some random bytes. Keep this really secret. TODO: load it from the environment
app.secret_key = b'_f9j38hfnu746bnakdk'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.route("/")
def index():
    if "username" in session:
        return render_template('index.html', username=session["username"])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            log_the_user_in(request.form['username'])
            return redirect(url_for('index'))
        else:
            app.logger.warning('Invalid login attempt',
                               request.form['username'],
                               request.form['password'])
            return render_template('login.html', error='Invalid username/password')
    else:
        return render_template('login.html', error=None)

def valid_login(username, password):
    log.info("Username="+username)
    log.info("Password="+password)
    user = User.query.filter_by(_username=username).first()
    return user is not None and user.password == password

def log_the_user_in(username):
     session["username"] = username

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("username")
    return redirect('login')

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html', person=name)

@app.route("/escaped")
def escaped():
    name = request.args.get("name","Flask")
    return f"Hello, {escape(name)}"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

# APIs
@app.route('/api/users', methods=['GET'])
def api_users():
    return jsonify(User.query.all())

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)