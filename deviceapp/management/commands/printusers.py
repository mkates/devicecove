from django.core.management.base import BaseCommand, CommandError
from deviceapp.models import BasicUser

class Command(BaseCommand):
    args = '<user_id user_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for user_id in args:
        	try:
        		user = BasicUser.objects.get(pk=int(user_id))
        	except BasicUser.DoesNotExist:
        		raise CommandError('User "%s" does not exist' % user_id)
        	self.stdout.write('Users id is "%s"' % user_id)