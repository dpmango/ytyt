from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import TokenProxy


admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
