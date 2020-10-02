import csv
import os
from tempfile import mkstemp
from wsgiref.util import FileWrapper

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, FormView, View

from conf_site.core.forms import CsvUploadForm


def csrf_failure(request, reason=""):
    """
    Custom view for users who encounter CSRF errors.

    https://docs.djangoproject.com/en/1.9/ref/settings/#csrf-failure-view

    When we upgrade to Django 1.10, this view can be removed.

    """
    response = TemplateResponse(
        request=request, template="403_csrf.html", status=403
    )
    return response


class CsvView(View):
    """A abstract view that returns a CSV file as a response."""

    http_method_names = ["get"]

    # Create generic names for required attributes.
    # This should be overwritten by inherited views.
    csv_filename = "export.csv"
    header_row = None

    def __init__(self, **kwargs):
        super(CsvView, self).__init__(**kwargs)

        self.temp_filename = mkstemp()[1]
        self.temp_file = open(
            file=self.temp_filename, mode="w", encoding="utf-8"
        )

        # Initialize CSV file.
        self.csv_writer = csv.writer(self.temp_file, dialect=csv.unix_dialect)
        if self.header_row:
            self.csv_writer.writerow(self.header_row)

    def get(self, *args, **kwargs):
        # Make sure that everything has been saved.
        self.temp_file.flush()
        os.fsync(self.temp_file.fileno())
        self.temp_file.close()
        # Push CSV to user.
        wrapper = FileWrapper(open(self.temp_filename))
        response = HttpResponse(wrapper, content_type="text/csv")
        response["Content-Disposition"] = (
            "attachment; filename=%s" % self.csv_filename
        )
        # Sending a Content-Length header gives the user better information
        # about the progress of their download.
        response["Content-Length"] = os.path.getsize(self.temp_filename)
        return response


class CsvImportView(FormView):
    form_class = CsvUploadForm
    http_method_names = ["get", "post"]

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            excel_file = request.FILES["csv_file"]
            # Save file to temporary folder. We only need it for
            # a short period of time.
            temp_file, filename = mkstemp(suffix=".csv")
            for chunk in excel_file.chunks():
                os.write(temp_file, chunk)
            os.fsync(temp_file)
            os.close(temp_file)
            self.process(filename, request.user.id)
            os.remove(filename)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def process(self, filename, user_id):
        pass


class SlugDetailView(DetailView):
    model = None
    view_name = None

    def get_object(self, queryset=None):
        # Use a custom queryset if provided.
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)

        # Only lookup object by its primary key, in case the
        # provided slug was incorrect.
        try:
            this_object = queryset.filter(pk=pk).get()
        except self.model.DoesNotExist:
            raise Http404()
        return this_object

    def render_to_response(self, context, **response_kwargs):
        this_object = self.get_object()

        # Verify that provided slug is correct.
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None and slug != this_object.slug:
            return redirect(
                to=self.view_name,
                pk=this_object.pk,
                slug=this_object.slug,
                permanent=True,
            )

        return super().render_to_response(context, **response_kwargs)


class SlugRedirectView(View):
    model = None
    redirect_view_name = None

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        try:
            this_object = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404()

        redirect_url = reverse(
            self.redirect_view_name,
            kwargs={"pk": this_object.pk, "slug": this_object.slug},
        )
        return HttpResponsePermanentRedirect(redirect_url)


class SuperuserOnlyView(UserPassesTestMixin, View):
    """A view which only allows access to superusers."""

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif not self.request.user.is_anonymous:
            # Non-anonymous, non-superuser users should see an error page.
            self.raise_exception = True
        return False


class TimeZoneChangeView(View):
    """
    A view that stores the user's time zone in the session.
    """

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        request.session["time_zone"] = request.POST["time_zone"]
        return HttpResponseRedirect(request.POST["next"])
