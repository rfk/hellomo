
import jwt
import requests

from django.conf import settings


OIDC_CONFIG_PATH = '/.well-known/openid-configuration'


class OIDCClient:

    def __init__(self, provider, client_id=None, client_secret=None, extra={}):
        self.provider = provider
        self.provider_info = requests.get(provider + OIDC_CONFIG_PATH).json()
        config = settings.OIDC_CLIENT_CONFIG.get(provider, {})
        if client_id is None:
            client_id = config.get('client_id')
        self.client_id = client_id
        if client_secret is None:
            client_secret = config.get('client_secret')
        self.client_secret = client_secret
        if extra is None:
            extra = config.get('extra')
        self.extra = extra.copy()

    def get_authorization_url(self, scope='openid', **kwds):
        url = self.provider_info['authorization_endpoint']
        url += '?scope=' + scope
        url += '&client_id=' + self.client_id
        url += '&state=' + kwds.pop('state', '')
        url += '&response_type=' + kwds.pop('response_type', 'code')
        for k,v in kwds.iteritems():
            url += '&' + k + '=' + v
        for k,v in self.extra.iteritems():
            url += '&' + k + '=' + v
        return url

    def redeem_authorization_code(self, code, **kwds):
        url = self.provider_info['token_endpoint']
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
        }
        for k,v in kwds.iteritems():
            body[k] = v
        for k,v in self.extra.iteritems():
            body[k] = v
        return requests.post(url, body).json()

    def get_user_info(self, access_token):
        url = self.provider_info['userinfo_endpoint']
        headers = { 'Authorization': 'Bearer ' + access_token }
        return requests.get(url, headers=headers).json()

