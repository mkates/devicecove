from django.http import HttpResponsePermanentRedirect
from django.conf import settings

########################################
####### Forces https:// sitewide #######
########################################

class SecureRequiredMiddleware(object):
    def __init__(self):
        #self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = getattr(settings, 'HTTPS_SUPPORT')
    def process_request(self, request):
        if self.enabled and not request.is_secure():
            request_url = request.build_absolute_uri(request.get_full_path())
            secure_url = request_url.replace('http://', 'https://')
            return HttpResponsePermanentRedirect(secure_url)
        return None

