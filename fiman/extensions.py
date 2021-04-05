from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor



db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()



# 由于session中只会存储登录用户的id，获取用户对象使用这一方法
# 当调用Flask-Login提供的current_user时，这一方法会自动调用并返回对应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from fiman.models import Admin
    user = Admin.query.get(int(user_id))
    return user

# 设置登录视图端点值
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"
login_manager.login_message = '请先登录'
