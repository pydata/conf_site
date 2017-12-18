from conf_site.cms.models import HomePage


def homepage_context(request):
    """
    Add homepage information into context.

    Add certain homepage fields into the general context so that they
    are available from all pages, regardless of whether they were
    generated with Wagtail or Symposion.
    """
    context = {}
    # Assume that the homepage is the root page in Wagtail.
    home_page = request.site.root_page.specific

    if home_page.seo_title:
        context["conference_title"] = home_page.seo_title
    else:
        context["conference_title"] = home_page.title
    # If the homepage is not a HomePage (see models.py), it
    # won't have any of these custom fields.
    if type(home_page) == HomePage:
        context["ticketing_url"] = home_page.ticketing_url
        context["footer_email"] = home_page.footer_email
        context["footer_twitter"] = home_page.footer_twitter

    return context
