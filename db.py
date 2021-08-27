import os
from pickle import dumps, loads
from base64 import b64encode as enc, b64decode as dec
from supabase_py import create_client


obj_to_text = lambda obj: enc(dumps(obj)).decode()
text_to_obj = lambda text: loads(dec(text.encode('utf-8')))


class DB:
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )

    @staticmethod
    def save_user(auth):
        DB.supabase.table('user_auth').insert({
            'token': auth.oauth_token,
            'userbin': obj_to_text(auth)
        }).execute()

    @staticmethod
    def get_user(token):
        json = DB.supabase.table('user_auth').select('userbin').eq('token', token).execute()
        if data := json.get('data', [None]):
            if data:
                return text_to_obj(data[0].get('userbin'))

    @staticmethod
    def get_token(cookie):
        json = DB.supabase.table('cookies').select('token').eq('cookie', cookie).execute()
        if data := json.get('data', [None]):
            if data:
                return data[0].get('token', None)

    @staticmethod
    def save_token(cookie, token):
        json = DB.supabase.table('cookies').insert({
            'cookie': cookie,
            'token': token
        }).execute()
        if data := json.get('data', [None]):
            if data[0]:
                return data[0]
    