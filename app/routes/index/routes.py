import hashlib
import logging
import faker

from flask import current_app as app, session, request, Response, redirect, url_for, abort, render_template, flash
from flask_login import current_user as worker, login_user, logout_user, login_required

from uuid import uuid4

from . import _ as bp, logging

from ...models.user import User
from ... import db

faker = faker.Faker()

@bp.route("/", methods=['GET'])
@bp.route("/relock", methods=['GET'])
def index():
    return render_template('index.html')

@bp.route("/verificated", methods=['GET','POST'])
def verificated():
    if id := request.device.owner:
        if user := User.query.filter_by(id=id).first():
            return render_template('verificated.html', id=request.form.get('id')
                                                     , server=request.form.get('server')
                                                     , public=request.form.get('public')
                                                     , token=request.form.get('X-Key-Token')
                                                     , signature=request.form.get('X-Key-Signature')
                                                     , xsid=request.form.get('xsid')
                                                     , screen=request.form.get('screen')
                                                     , verify=request.device.confirm() if request.method == 'POST' else False
                                                     , email=user.get_email()
                                                     , owner=user.get_id())
    return redirect(url_for('index.index'))

@bp.route("/fresh", methods=['GET','POST'])
def fresh():
    return render_template('fresh.html', id=request.form.get('id')
                                       , server=request.form.get('server')
                                       , public=request.form.get('public')
                                       , token=request.form.get('X-Key-Token')
                                       , signature=request.form.get('X-Key-Signature')
                                       , xsid=request.form.get('xsid')
                                       , screen=request.form.get('screen')
                                       , verify=request.device.confirm() if request.method == 'POST' else False
                                       , owner=None)

@bp.route("/anonymous", methods=['GET','POST'])
def anonymous():
    return render_template('anonymous.html', id=request.form.get('id')
                                           , server=request.form.get('server')
                                           , public=request.form.get('public')
                                           , token=request.form.get('X-Key-Token')
                                           , signature=request.form.get('X-Key-Signature')
                                           , xsid=request.form.get('xsid')
                                           , screen=request.form.get('screen')
                                           , verify=request.device.confirm() if request.method == 'POST' else False
                                           , owner=None)

@bp.route("/confirm", methods=['POST'])
@bp.route("/confirm/<string:device>/<string:token>/<string:signature>", methods=['GET'])
def confirm(device=str(), token=str(), signature=str()):
    if request.method == 'POST':
        device    = request.form.get('device', str())
        token     = request.form.get('token', str())
        signature = request.form.get('signature', str())

@bp.route("/signin", methods=['POST'])
@bp.route("/signin/<string:xsid>/<string:id>/<string:email>", methods=['GET'])
def signin(xsid=str(), id=str(), email=str()):
    if request.method == 'POST':
        xsid  = request.json.get('xsid', str())
        id    = request.json.get('id', str())
        email = request.json.get('email', str())
    print(xsid, id, email)
    with app.relock.tcp(**{'route': 'user_logged_in',
                            'sid': session.sid,
                            'rid': str(uuid4()),
                            'user': id,
                            'email': email,
                            'authenticated': False,
                            'active': True,
                            'anonymous': False,
                            'host': app.config.get('SERVER_HOST')}) as tcp:
        return dict(status=tcp.response)
    return dict(status=423)

@bp.route("/signout", methods=['POST'])
@bp.route("/signout/<string:device>/<string:id>/<string:email>", methods=['GET'])
def signout(device=str(), id=str(), email=str()):
    if request.method == 'POST':
        device = request.json.get('device', str())
        id     = request.json.get('id', str())
        email  = request.json.get('email', str())
    with app.relock.tcp(**{'route': 'user_logged_out',
                           'sid': xsid,
                           'rid': str(uuid4()),
                           'addr': request.remote_addr,
                           'host': app.config.get('SERVER_HOST')}) as tcp:
        return dict(status=tcp.response)
    return dict(status=423)

@bp.route("/create", methods=['POST'])
def create(email=str()):
    if id := request.device.owner:
        if user := User.query.filter_by(id=id).first():
            user.login()
    elif user := User(email=faker.email(),
                      password=faker.password(16)):
        user.key = hashlib.blake2b(user.email.encode(),
                                   salt=user.get_id().to_bytes(16, byteorder='big'),
                                   digest_size=16).hexdigest()
        user.save()
        db.session.commit()
        user.login()
    if worker.is_authenticated:
        if email := worker.email:
            worker.logout()
    return dict(username=email)