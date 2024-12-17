from flask import Blueprint, render_template, request, redirect, url_for
from models.item import Item

# Blueprintの作成
item_bp = Blueprint('item', __name__, url_prefix='/item')


@item_bp.route('/')
def list():
    item = Item.select()
    return render_template('item_list.html', title='装備一覧', items=item)


@item_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        hitpoint = request.form['hitpoint']
        attack = request.form['attack']
        defence = request.form['defence']
        Item.create(name=name, hitpoint=hitpoint,attack=attack,defence=defence)
        return redirect(url_for('item.list'))
    
    return render_template('item_add.html')


@item_bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = Item.get_or_none(Item.id == item_id)
    if not item:
        return redirect(url_for('item.list'))

    if request.method == 'POST':
        item.name = request.form['name']
        item.hitpoint = request.form['hitpoint']
        item.attack = request.form['attack']
        item.defence = request.form['defence']
        item.save()
        return redirect(url_for('item.list'))

    return render_template('item_edit.html', item=item)