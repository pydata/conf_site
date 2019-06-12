from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token",
                        request.session["pending-token"])
    return render(request, "dashboard.html")
