from django.shortcuts import redirect
from django.contrib import messages

def csrf_failure(request, reason=""):
    messages.error(request, "Security check failed or session expired. Please refresh and try again.")
    # Redirect back to the login page or referring page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('authentication:login')
