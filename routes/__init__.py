from .user import user_bp
from .item import item_bp
from .status import status_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  item_bp,
  status_bp
]
