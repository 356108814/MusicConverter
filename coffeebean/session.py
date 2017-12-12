# encoding: utf-8
"""
session支持https://github.com/mmejia27/tornado-memcached-sessions/blob/master/session.py
@author Yuriseus
@create 2016-8-1 14:39
"""
import hashlib
import hmac
import pickle
import uuid

from .cache import Cache


class SessionData(dict):
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key


class Session(SessionData):
    def __init__(self, session_manager, request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler

        try:
            current_session = session_manager.get(request_handler)
        except InvalidSessionException:
            current_session = session_manager.get()

        for key, data in current_session.items():
            # self[key] = data
            super(Session, self).__setitem__(key, data)
        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

    def __setitem__(self, key, value):
        super(Session, self).__setitem__(key, value)
        self.session_manager.set(self.request_handler, self)

    def __getitem__(self, key):
        if key in self:
            return super(Session, self).__getitem__(key)
        else:
            return None


class SessionManager(object):
    def __init__(self, secret=None, session_timeout=None):
        if not secret:
            secret = '2d50Y8xa3W3h'
        if not session_timeout:
            session_timeout = 7200
        self.secret = secret
        self.session_timeout = session_timeout

        self.cache = Cache.current()

    def get(self, request_handler=None):

        if request_handler is None:
            session_id = None
            hmac_key = None
        else:
            session_id = request_handler.get_secure_cookie('session_id')
            hmac_key = request_handler.get_secure_cookie('verification')

        if session_id is None:
            session_exists = False
            session_id = self._generate_id()
            hmac_key = self._generate_hmac(session_id)
        else:
            session_exists = True

        check_hmac = self._generate_hmac(session_id)
        if isinstance(hmac_key, bytes):
            hmac_key = hmac_key.decode()
        if hmac_key != str(check_hmac):
            raise InvalidSessionException()

        session = SessionData(session_id, hmac_key)

        if session_exists:
            session_data = self._fetch(session_id)
            for key, data in session_data.items():
                session[key] = data

        return session

    def set(self, request_handler, session):
        request_handler.set_secure_cookie('session_id', session.session_id)
        request_handler.set_secure_cookie('verification', session.hmac_key)
        session_data = pickle.dumps(dict(session.items()), pickle.HIGHEST_PROTOCOL)
        self.cache.setex(session.session_id, self.session_timeout, session_data)

    def _fetch(self, session_id):
        try:
            session_data = raw_data = self.cache.get(session_id)
            if raw_data is not None:
                self.cache.setex(session_id, self.session_timeout, raw_data)
                session_data = pickle.loads(raw_data)
            if isinstance(session_data, dict):
                return session_data
            else:
                return {}
        except IOError:
            return {}

    def _generate_id(self):
        new_id = hashlib.sha256((self.secret + str(uuid.uuid4())).encode())
        return new_id.hexdigest()

    def _generate_hmac(self, session_id):
        if isinstance(session_id, str):
            session_id = session_id.encode()
        return hmac.new(session_id, self.secret.encode(), hashlib.sha256).hexdigest()


class InvalidSessionException(Exception):
    pass
