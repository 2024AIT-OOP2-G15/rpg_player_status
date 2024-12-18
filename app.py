import math
from flask import Flask, render_template
from models import initialize_database, Status
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # 全てのStatusレコードを取得
    status_list = Status.select()

    # Chart.js用データの準備
    chart_data = {
        "labels": [],  # キャラ名やID
        "datasets": [
            {
                "label": "総合ステータス",  # グラフのラベル
                "data": [],  # 各キャラの総合ステータス値
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            }
        ],
    }

    # 各キャラの総合ステータスを計算してChart.jsデータに追加
    for s in status_list:
        # キャラ名またはIDをラベルに使用
        chart_data["labels"].append(s.name if hasattr(s, 'name') else f"ID {s.id}")
        # 総合ステータスの計算
        total_status = s.hp + s.at + s.df
        chart_data["datasets"][0]["data"].append(total_status)

    # Statusデータベースを全て取得、格納
    sList = []
    for i in range(len(Status)):
        sList.append(Status.get(Status.id == i+1))

    # キャラの使用率の取得、送信
    chara_unique = set([chara for chara in [st.name.name for st in sList]]) # キャラ名の一意のリスト(被りがない)
    chara_using = [chara for chara in [st.name.name for st in sList]] # 使用キャラのリスト(実際に使われてるキャラ)
    chara_usagerate = [math.floor(chara_using.count(chara)/len(sList)*100) for chara in chara_unique] # キャラごとの使用率
    # リストの結合、ソート
    chara_pair = list(zip(chara_unique,chara_usagerate))
    chara_unique_sorted, chara_usagerate_sorted = zip(*sorted(chara_pair))
    chara_use_data = {
        "type":'doughnut',
        "data": {
            "labels": [name for name in chara_unique_sorted], # 武器の名前
            "datasets": [
                {
                    "label": "使用率",
                    "data": chara_usagerate_sorted,  # 武器の使用率
                }
            ]
        },
        "options": {
            "plugins": {
                "title": {
                    "display": "true",
                    "text": '冒険者の人気度',
                    "font": {
                        "size": 30
                    }
                }
            }
        }
    }

# Statusテーブルからデータを取得
    statuslist = []
    for i in range(len(Status)):
        statuslist.append(Status.get(Status.id == i+1))

    # アイテム名だけをリストに収集し、setで一意のリストを作成
    items = [status.item.name for status in statuslist]
    unique_weapons = list(set(items))  # 重複しない武器名のリストを取得
    
    # 各武器ごとのカウント用辞書を初期化
    weapon_count = {weapon: 0 for weapon in unique_weapons}

    # 武器の出現数をカウント
    for item in items:
        if item in weapon_count:
            weapon_count[item] += 1

    # 総アイテム数の取得
    total_items = len(items)

    # 分母が0の場合の対策
    if total_items == 0:
        weapon_ratio = {weapon: 0 for weapon in unique_weapons}
    else:
        weapon_ratio = {
            weapon: math.floor((count / total_items) * 1000) / 10
            for weapon, count in weapon_count.items()
        }

    # グラフ用のデータ
    chart_labels = list(weapon_ratio.keys())
    chart_data = list(weapon_ratio.values())

    item_use_raito = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'chart_title': "武器使用割合",
        'chart_target': "装備データ"
    }

    return render_template('index.html', chart_data=chart_data, chara_use_data=chara_use_data, item_use_raito=item_use_raito)

if __name__ == '__main__':
    app.run(port=8800,debug=True)