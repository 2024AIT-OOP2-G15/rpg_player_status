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

    # Chart.js用データをテンプレートに渡す
    return render_template('index.html', chart_data=chart_data)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
