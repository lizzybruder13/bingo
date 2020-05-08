from flask import Flask, render_template, request, session, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Player

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "SECRET_KEY"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""
    return render_template('homepage.html')

@app.route('/player')
def player_info():
    """Get player info and pass to new route"""
    player_name = request.args.get('name')
    password = request.args.get('password')
    if password == 'bruder2020': 
        player = Player(player_name=player_name, password=password)
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('player', name=player.player_name))
    if password == 'lizhost':
        return redirect(url_for('player', name='host'))
    else:
        return redirect('/')

@app.route('/player/<name>')
def player(name):
    """Individual Players Page"""
    return render_template('player.html', name=name)

@app.route('/host')
def host():
    """host controls"""
    return render_template('host.html')

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')