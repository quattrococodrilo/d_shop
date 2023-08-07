from django.contrib import admin

class AdminSiteSettingsMixin(admin.AdminSite):
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adminsite-objects
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adminsite-attributes

    # "Django site admin" Populates the <title> tag on each page of
    # the admin interface.
    site_title = "Fly Admin"

    # "Django administration" Sets the header on the login form.
    site_header = "Fly Administration"

    # The link to use for the View Site option (defaults to /). 
    # This is overridden when the site runs on a custom path, 
    # and the redirection should take the user to the sub-path directly.
    # site_url: str =  "/"

    # "Site administration" Sets the heading on the admin index page
    # (where the models are listed).
    index_title = "Fly Site Admin"

    # Provides the path to find the admin index template. If unset,
    # the admin/index.html template is used.
    # index_template = "admin/index.html"

    # Provides the path to find the app admin index template. If unset,
    # the admin/app_index.html template is used.
    # app_index_template = "admin/app_index.html"

    # Provides the path to find the login template.
    # If unset, the admin/login.html template is used.
    login_template = "admin/login.html"

    # Provides the path to find the logout template. If unset, the
    # registration/logged_out.html template is used.
    logout_template = "admin/logged_out.html"

    # Provides the path to find the password change template. If unset,
    # the registration/password_change_form.html template is used.
    # password_change_template = "admin/password_change_form.html"

    # Provides the path to find the password change done template. If unset,
    # the registration/password_change_done.html template is used.
    # password_change_done_template = "admin/password_change_done.html"
