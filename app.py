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

    # ステータスの合計値を計算
    total_hp = sum(s.hp for s in status_list)
    total_at = sum(s.at for s in status_list)
    total_df = sum(s.df for s in status_list)

    # 合計とステータスリストをテンプレートに渡す
    return render_template(
        'index.html',
        status=status_list,
        total_hp=total_hp,
        total_at=total_at,
        total_df=total_df
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)