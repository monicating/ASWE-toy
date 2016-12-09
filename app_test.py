import os
import app as flaskr
import unittest
import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sqlalchemy

import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

        self.app.engine = sqlalchemy.create_engine('mysql://root:mysql@127.0.0.1')
        self.app.engine.execute("USE HMU_TEST")

        flaskr.app.config['MYSQL_DATABASE_DB'] = 'HMU_TEST'
        flaskr.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@127.0.0.1/HMU_TEST'


    def tearDown(self):
        self.app.engine.execute("TRUNCATE TABLE TBL_USER")

        
    def signUp(self, name, email, password):
        return self.app.post('/signUp', data=dict(
            inputName=name, 
            inputEmail=email, 
            inputPassword=password
            ), follow_redirects=True)


    def test_signUp(self):
        #user email has not been created
        rv = self.signUp('User1', 'user1@columbia.edu', 'password')
        assert "User created successfully" in rv.data
        #print(rv.data)

        #user email has already been created
        rv = self.signUp('User1', 'user1@columbia.edu', 'password')
        assert "Username Exists" in rv.data
        
        #username too long
        rv = self.signUp('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'user2@columbia.edu', 'password')
        assert "Data too long" in rv.data
        
        #email too long
        rv = self.signUp('User3', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@columbia.edu', 'password')
        assert "Data too long" in rv.data
        
        #password too long
        rv = self.signUp('User4', 'user4@columbia.edu', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        assert "Data too long" in rv.data




if __name__ == '__main__':
    unittest.main()