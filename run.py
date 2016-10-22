# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash ,redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///npb.sqlite'
app.config['SECRET_KEY'] = 'xNVg}f_m:UmiOB{9bC`SvB9j5N<-3I./'
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    dates = db.Column(db.Date, nullable=False)
    home = db.Column(db.Text)
    away = db.Column(db.Text)
    start = db.Column(db.String, nullable=False)
    stadium = db.Column(db.String, nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    home_starter = db.Column(db.String, nullable=False)
    away_starter = db.Column(db.String, nullable=False)
    home_id = db.Column(db.Integer, nullable=False)
    away_id = db.Column(db.Integer, nullable=False)
    bikou = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)


class Stadium(db.Model):
    __tablename__ = 'stadium'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    abbr = db.Column(db.String)
    bikou = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    abbr = db.Column(db.String)
    league = db.Column(db.Integer)
    bikou = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)


class TeamStat(db.Model):
    __tablename__ = 'team_stats'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    draw = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)



@app.route("/")
def index():
    games = Game.query.\
        with_entities(
            Game.id,
            Game.dates,
            Game.stadium,
            Game.start,
            Game.home,
            Game.away,
            Game.home_starter,
            Game.away_starter,
            Game.home_score,
            Game.away_score,
            db.func.strftime('%m', Game.dates).label('month')).\
        order_by('month', Game.dates.asc()).all()

    import itertools
    sort_obj = sorted(games, key=lambda x: x.month)
    group_by_dates = itertools.groupby(sort_obj, key=lambda x: x.month)

    return render_template('index.html', games=group_by_dates)


@app.route("/score")
def score():
    dates = request.args.get('dates', '')
    games = Game.query.filter(Game.dates == dates).all()
    return render_template('score.html', games=games, dates=dates)


@app.route("/update_score", methods=['POST'])
def update_score():
    games = request.form.getlist('games[]')
    home_score = request.form.getlist('home_score[]')
    away_score = request.form.getlist('away_score[]')

    game_list = []

    for (id, hm, aw) in zip(games, home_score, away_score):
        od = Game.query.filter(Game.id == id).one()
        od.home_score = hm
        od.away_score = aw
        game_list.append(od)

    db.session.add_all(game_list)
    db.session.commit()
    flash(u'スコアを登録しました')

    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
