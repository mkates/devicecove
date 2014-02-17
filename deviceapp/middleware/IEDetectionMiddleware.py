import re
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context, loader

class IEDetectionMiddleware(object):
    """
    middleware to detect if the user is on old IE
    """
    def process_request(self, request):
        is_ie = False
         
        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
         
        # Test IE 1-7
        pattern = "msie [1-9]\."
        prog = re.compile(pattern, re.IGNORECASE)
        match = prog.search(user_agent)
         
        if match:
            is_ie = True # NOOOOOO
         
        if is_ie == True:
            return render_to_response('general/ieupgrade.html',context_instance=RequestContext(request))