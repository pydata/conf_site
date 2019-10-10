from wagtail.core import hooks


@hooks.register("construct_page_action_menu")
def remove_submit_to_moderator_option(menu_items, request, context):
    # https://docs.wagtail.io/en/v2.6.2/reference/hooks.html#construct-page-action-menu
    menu_items[:] = [
        item for item in menu_items if item.name != "action-submit"
    ]
