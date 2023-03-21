from flask import render_template, Blueprint

# здесь сразу и вьюшка и путь

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html')

