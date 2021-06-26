from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordResetTokenGeneratorWithoutLastLogin(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key and some user state that's sure to change
        after a password reset to produce a token that invalidated when it's
        used:
        1. The password field will change upon a password reset (even if the
           same password is chosen, due to password salting).
        2. The last_login field will usually be updated very shortly after
           a password reset.
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.

        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.

        UPDATE VERSION: Удалено использоватение последнего логина в системе, так как это
                        значение может мешать в момент декодирования, если пользователь после зашел в систему
        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        return str(user.pk) + user.password + str(timestamp)


token_generator = PasswordResetTokenGeneratorWithoutLastLogin()
