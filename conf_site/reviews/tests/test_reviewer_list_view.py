from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.tests import ReviewingSuperuserMixin


class ReviewerListViewTestCase(ReviewingSuperuserMixin, AccountsTestCase):
    reverse_view_name = "reviewer_list"
    reverse_view_args = None
