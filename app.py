from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from forms import NameForm
import os



app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

basedir = os.path.abspath(app.root_path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
        # name = form.name.data
        # form.name.data = ''
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


@app.route('/user/')
@app.route('/user/<name>/')
def user(name=None):
    return render_template('user.html', user=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_sever_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=8777)