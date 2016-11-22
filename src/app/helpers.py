from flask import flash, url_for
from datetime import datetime


def submit_to(url):
    return "javascript:submit_form('{0}');".format(url)

def required(field):
    return u"El campo {field} es requerido".format(field=field)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % error)
