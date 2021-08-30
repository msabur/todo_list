from . import app, nav
from flask_login import current_user
from flask_nav.elements import View, Navbar


@nav.navigation()
def navbar():
    items = [View("Home", "index")]
    if current_user.is_authenticated:
        items.extend([View("Profile", "profile"), View("Log Out", "logout")])
    else:
        items.extend([View("Log in", "login"), View("Register", "register")])
    return Navbar(app.config.get("SITE_NAME"), *items)