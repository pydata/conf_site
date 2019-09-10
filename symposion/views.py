from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from symposion.schedule.models import Schedule


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token",
                        request.session["pending-token"])
    context = {"schedules": Schedule.objects.all()}
    return render(request, "dashboard.html", context)
