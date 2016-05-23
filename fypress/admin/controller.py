# -*- coding: UTF-8 -*-
from functools import wraps
from flask import Blueprint, session, request, redirect, url_for, render_template
from .. user import login_required

admin = Blueprint('admin', __name__,  url_prefix='/admin')


@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')
