"""
Form view.

URLs include:
/form
/insert

"""
import flask
import learning
from flask_login import (
        current_user,
        login_required,
)
from learning.views.matches import matches
from learning.db import get_conn
from learning.user import User

conn = get_conn()

def insert_details(id_,name,email,north,central,gender,gender_pref,major,year,clubs,eecs_203,eecs_280,avg_hours,hours,grade,career):
    cur = conn.cursor()
    # Check if id already exists in Details table
    # If so, update the row
    cur.execute("SELECT * FROM Details WHERE id = %s", (id_,))
    user_obj = cur.fetchone()
    if user_obj:
        # Update the existing row
        cur.execute("UPDATE Details SET north=%s,central=%s,gender=%s,gender_pref=%s,major=%s,year=%s,clubs=%s,eecs_203=%s,eecs_280=%s,avg_hours=%s,hours=%s,grade=%s,career=%s WHERE id=%s",
            (north,central,gender,gender_pref,major,year,clubs,eecs_203,eecs_280,avg_hours,hours,grade,career,id_))
        conn.commit()
    else:
        # Insert a new row
        cur.execute("INSERT INTO Details (id,name,email,north,central,gender,gender_pref,major,year,clubs,eecs_203,eecs_280,avg_hours,hours,grade,career) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (id_,name,email,north,central,gender,gender_pref,major,year,clubs,eecs_203,eecs_280,avg_hours,hours,grade,career))
        conn.commit()

def get_details():
    cur = conn.cursor()
    cur.execute("SELECT *  FROM Details")
    details = cur.fetchall()
    return details

@learning.app.route("/form")
@login_required
def form():
    context = {"name": current_user.name, "email": current_user.email}
    return flask.render_template("form.html", **context)


@learning.app.route("/insert", methods=['POST'])
@login_required
def insert():
    if flask.request.method == 'POST':
        id_ = current_user.id
        name = flask.request.form['name']
        email = flask.request.form['email']
        # south = flask.request.form['south']
        gender = flask.request.form['gender']
        gender_pref = flask.request.form['gender_pref']
        major = flask.request.form['major']
        year = flask.request.form['year']
        clubs = flask.request.form['clubs']
        north = 0
        central = 0
        eecs_280 = 0
        eecs_203 = 0
        if "north" in flask.request.form:
            north = 1
        if "central" in flask.request.form:
            central = 1
        if "eecs_280" in flask.request.form:
            eecs_280 = 1
        if "eecs_203" in flask.request.form:
            eecs_280 = 1
        # eecs_281 = flask.request.form['eecs_281']
        # eecs_370 = flask.request.form['eecs_370']
        # eecs_376 = flask.request.form['eecs_376']
        # eecs_388 = flask.request.form['eecs_388']
        # eecs_481 = flask.request.form['eecs_481']
        # eecs_482 = flask.request.form['eecs_482']
        # eecs_492 = flask.request.form['eecs_492']
        avg_hours = flask.request.form['avg_hours']
        hours = flask.request.form['hours']
        grade = flask.request.form['grade']
        career = flask.request.form['career']

        insert_details(id_,name,email,north,central,gender,gender_pref,major,year,clubs,eecs_203,eecs_280,avg_hours,hours,grade,career)
        details = get_details()

        # match = MatchesAPI(details)
        # matchings = match.matched_table

        # for match in matchings:
        #     insert_matches(match[0],match[1],match[2],match[3],match[4],match[5],match[6],match[7],match[8],match[9],match[10],match[11],match[12],match[13],match[14])
        # print(details)

        context = {"name": name, "email": email, "details": details}
        return flask.render_template('form.html',**context)
