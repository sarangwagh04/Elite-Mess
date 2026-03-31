from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Suggestion
from django.contrib import messages

@login_required
def submit_suggestion(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Suggestion.objects.create(user=request.user, text=text)
            messages.success(request, 'Feedback submitted!')
        else:
            messages.error(request, 'Please enter some text.')
    
    return redirect('billing:student_dashboard')

@login_required
def view_suggestions(request):
    # This view will be used if someone goes directly to /suggestions/view/
    # But dashboards already include this.
    suggestions = Suggestion.objects.all().order_by('-created_at')
    return render(request, 'suggestions/view_suggestions.html', {'suggestions': suggestions})
