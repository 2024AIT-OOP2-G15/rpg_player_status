from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models import User, Item, Status
import math

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)
    
# ホームページのルート
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():

    # Statusテーブルからデータを取得
    # statuses = Status.select()
    # print (statuses)
    statuslist = []
    for i in range(len(Status)):
       statuslist.append(Status.get(Status.id == i+1))

    # デバッグ用
    #    print ("status:" + statuslist)
    
    # アイテム名だけをリストに収集
    items = [status.item.name for status in statuslist]
    ## デバッグ用
    # print (items)

    swordcount = 0
    shieldcount = 0
    canecount = 0
    other = 0
    total_items = len(items)

    for i in range(len(items)):  # 修正箇所
        print (items[i])
        if items[i] == "剣":
            swordcount += 1
        elif items[i] == "盾":
            shieldcount += 1
        elif items[i] in ["杖", "つえ"]:  # 条件式を修正
            canecount += 1
        else:
            other += 1
    
    # デバッグ用
    print (shieldcount)
    # 分母が0の場合の対策
    total_items = len(items)
    # デバッグ用
    # print (total_items)
    if total_items == 0:
        swordratio = shieldratio = caneratio = otherratio = 0
    else:
        swordratio = (swordcount / total_items) * 100
        shieldratio = (shieldcount / total_items) * 100
        caneratio = (canecount / total_items) * 100
        otherratio = (other / total_items) * 100

        swordratio = math.floor(swordratio * 10) / 10
        shieldratio = math.floor(shieldratio * 10) / 10
        caneratio = math.floor(caneratio * 10) / 10
        otherratio = math.floor(otherratio * 10) / 10

    # デバッグ用
    # print (swordratio)
    # print (shieldratio)
    # print (caneratio)
    # print (otherratio)

    ratio = [swordratio, shieldratio, caneratio, otherratio]

    c = {
        'chart_labels': items,
        'chart_data': ratio,
        'chart_title': "武器使用割合",
        'chart_target': "タイトル"
    }
    
    # テンプレートにアイテム名リストを渡す
    return render_template('index.html', c=c)

if __name__ == '__main__':
    app.run(debug=True)