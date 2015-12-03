
import jwt
import requests

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from hellomo.oidc import OIDCClient


CLIENTS = {
    # Use FxA as the fallback IdP
    '': OIDCClient('https://oidc.dev.lcip.org'),
    # Use Google hosted-domain auth for @mozilla.com accounts
    'mozilla.com': OIDCClient(
        'https://accounts.google.com',
        extra={ 'hd': 'mozilla.com' },
    ),
}


def oidc_get_client(email):
    """Pick the appropraite OIDC provider based on email address."""
    domain = email.rsplit("@")[-1]
    try:
        return CLIENTS[domain]
    except KeyError:
        return CLIENTS['']
    

def root(request):
    return render(request, 'root.html')


def logout(request):
    del request.session['identity']
    return redirect(reverse(root))


def hello(request):
    if 'identity' in request.session:
        return render(request, 'hello.html')
    return oidc_begin(request)


def oidc_begin(request):
    email = request.POST['email']
    request.session['state'] = email  # XXX TODO: security and stuff...
    client = oidc_get_client(email)
    return redirect(client.get_authorization_url(
        scope='openid+profile',
        state=request.session['state'],
        redirect_uri=request.build_absolute_uri(reverse(oidc_complete)),
        login_hint=email,
    ))


def oidc_complete(request):
    if request.session['state'] != request.GET['state']:
       raise ValueError('state token mis-match')
    email = request.session['state']
    client = oidc_get_client(email)
    # If we used response_type="code id_token" we'd get the id_token
    # directly in the GET parameters...
    tokens = client.redeem_authorization_code(
        code=request.GET['code'],
        redirect_uri=request.build_absolute_uri(reverse(oidc_complete)),
    )
    # There are security things we should probably check here:
    #   * issuer is as expected
    #   * google "hosted domain" is correct
    identity = jwt.decode(tokens['id_token'], verify=False)
    info = client.get_user_info(tokens['access_token'])
    identity.update(info)
    if identity['email'].endswith('@mozilla.com'):
        identity['is_staff'] = True
    request.session['identity'] = identity
    return redirect(hello)
