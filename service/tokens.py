from django.contrib.auth.tokens import PasswordResetTokenGenerator
from typing import TypeVar

T = TypeVar('T')




class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            T.text_type(user.pk) + T.text_type(timestamp) +
            T.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()

