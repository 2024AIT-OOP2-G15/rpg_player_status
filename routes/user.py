from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    
    # データ取得
    users = User.select()

    return render_template('user_list.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():  
    if request.method == 'POST':
        name = request.form['name']
        hp = request.form['hp']
        at = request.form['at']
        df = request.form['df']
        User.create(name=name, at=at , df=df, hp=hp)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.hp = request.form['hp']
        user.at = request.form['at']
        user.df = request.form['df']
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)