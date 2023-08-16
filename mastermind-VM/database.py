# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# # from player import player


# db = None
# def init_db(app):
#     tables_to_create = ['player']
#     config_tables(app, tables_to_create)
    

# def config_tables(app, list_of_tables):
#     for table in list_of_tables:
#         config_table(app, table)

# def config_table(app, table_name):
#     with app.app_context():
#         __table_name = table_name
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}.sqlite3'.format(__table_name)
#         db = SQLAlchemy(app)
#         print(type(db))
#         db.create_all()

# # ------------ Classes ------------------------
# if(db != None):
#     class player(db.Model):
#         _nickname = db.Column('nickname', db.String(100), primary_key=True)

#         def __init__(self, _nickname):
#             self._nickname = _nickname