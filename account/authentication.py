from django.contrib.auth import get_user_model


class EmailAuthBackend:
    """
    This is a backend only for testing purposes. It shows how to use the authentication
    system. You can login using an e-mail address.
    """

    def authenticate(self, request, username=None, password=None):
        user = get_user_model()

        try:
            user = user.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user.DoesNotExist, user.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user = get_user_model()

        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None
