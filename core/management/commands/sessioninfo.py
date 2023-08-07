from pprint import pformat
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "List all user sessions and the data that they contain."

    def handle(self, *args, **options):
        session_store = SessionStore()
        for session in Session.objects.all():
            data = session_store.decode(session.session_data)
            user = get_user_model().objects.get(id=data['_auth_user_id'])
            self.stdout.write(
                    f"Session Key: {session.session_key}\n" 
                    f" User: {user.id} {user.username}\n"               
                    f" {user.email}\n"
            )
            self.stdout.write(pformat(data)) 
