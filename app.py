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

    # キャラごとの最終ステータス合計を計算
    chart_data = {
        "labels": [],  # キャラ名やIDを格納するリスト
        "datasets": [
            {
                "label": "HP",
                "data": [],
                "backgroundColor": "rgba(255, 99, 132, 0.5)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 1,
            },
            {
                "label": "AT",
                "data": [],
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            },
            {
                "label": "DF",
                "data": [],
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            },
        ],
    }

    for s in status_list:
        # キャラ名またはIDをラベルとして使用
        chart_data["labels"].append(s.name if hasattr(s, 'name') else f"ID {s.id}")
        # HP, AT, DFのデータを各データセットに追加
        chart_data["datasets"][0]["data"].append(s.hp)
        chart_data["datasets"][1]["data"].append(s.at)
        chart_data["datasets"][2]["data"].append(s.df)

    # Chart.js用データをテンプレートに渡す
    return render_template('index.html', chart_data=chart_data)


if __name__ == '__main__':
    app.run(port=8080, debug=True)