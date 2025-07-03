from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Import this

@login_required # This decorator ensures only logged-in users can access this page
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})