from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET'])
def admin_route():
    return render_template('index.html')
