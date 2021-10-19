"""
Match results main view.

URLs include:
matches
"""
import flask
import learning
import re

from learning.db import get_conn
from flask_login import login_required, current_user

conn = get_conn()

@learning.app.route("/matches")
@login_required
def matches():
    cur = conn.cursor()
    cur.execute("SELECT matches FROM Matches2 WHERE id = %s", (current_user.id))
    result = cur.fetchone()
    if result is None:
        flask.flash("Please fill out the form first. If you have done so already, please check back later for match updates.")
        return flask.redirect(flask.url_for("show_index"))
    matches = re.split(r'\t+', result[0].rstrip('\t'))

    match_infos = []
    for match in matches:
        match_tuple = tuple(match.split(','))
        cur.execute("SELECT name,email FROM Details WHERE id = %s", (match_tuple[0]))
        # match_info contains name,email,sim_score
        match_info = list(cur.fetchone())
        match_info.append(match_tuple[1])
        match_infos.append(match_info)
    context = {"match_infos": match_infos}
    return flask.render_template("matches.html", **context)
