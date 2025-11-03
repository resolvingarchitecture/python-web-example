from flask import Flask
from flask import make_response
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.route("/")
def index():
    username = request.cookies.get('username')
    if username:
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            return render_template('login.html', error='Invalid username/password')
    else:
        return render_template('login.html', error=None)

def valid_login(username, password):
    return username=='User' and password=='123'

def log_the_user_in(username):
     resp = make_response(render_template('home.html', username=username))
     resp.set_cookie('username', username)
     return resp

@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(render_template('login.html'))
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)