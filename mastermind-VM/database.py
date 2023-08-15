from flask import Flask
from flask_sqlalchemy import SQLAlchemy


__table_name = ''
def init_db():
    pass

def config_tables(list_of_tables):
    pass

def config_table(app,table_name):
    with app.app_context():
        __table_name = table_name
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}.sqlite3'.format(__table_name)
        db = SQLAlchemy(app)
        db.create_all()

# ----------------- TODO this should be a separate file! --------------------------------------
# class nicknames(db.Model):
#     _nickname = db.Column('name', db.String(100), primary_key=True)

#     def __init__(self, _nickname):
#         self._nickname = _nickname
# ------------------------------ END SECTION --------------------------------------------------
