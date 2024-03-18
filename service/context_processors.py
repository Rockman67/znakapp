from django.conf import settings

def account_settings(request):
    return {
        'ACCOUNT_EMAIL_VERIFICATION_TEMPLATE': settings.ACCOUNT_EMAIL_VERIFICATION_TEMPLATE,
    }

def account_exists_settings(request):
    return {
        'ACCOUNT_EMAIL_EXISTS_TEMPLATE': settings.ACCOUNT_EMAIL_EXISTS_TEMPLATE,
    }
