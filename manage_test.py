from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sqlalchemy

app = Flask(__name__)

engine = sqlalchemy.create_engine('mysql://root:mysql@127.0.0.1') # connect to server
engine.execute("DROP SCHEMA IF EXISTS HMU_TEST") 
engine.execute("CREATE SCHEMA HMU_TEST") 
engine.execute("USE HMU_TEST")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@127.0.0.1/HMU_TEST'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class tbl_user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45))
    user_username = db.Column(db.String(45), unique=True)
    user_password = db.Column(db.String(45))

sp_createUser = """
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END
"""

engine.execute(sp_createUser)

if __name__ == '__main__':
    manager.run()