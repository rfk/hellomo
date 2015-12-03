from django.conf.urls import url

import hellomo.views

urlpatterns = [
    url(r'^$', hellomo.views.root),
    url(r'^hello/$', hellomo.views.hello),
    url(r'^logout/$', hellomo.views.logout),
    url(r'^oidc/complete$', hellomo.views.oidc_complete),
]
