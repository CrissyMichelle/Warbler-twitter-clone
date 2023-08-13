"""Message model tests."""
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message

# python -m unittest test_message_model.py 
# and Terminal will run the following tests

# first, set up environmental variable to use a different testing db
os.environ['DATABASE_URL'] = "postgresql:///testwarbler"
# now we can import app
from app import app

# create tables and test case assertions
db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages"""
    
    def setUp(self):
        """Create test client and add sample data"""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()
    
    def tearDown(self):
        """Results in rolling back all changes performed during testing"""
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Does basic message model work?"""

        m = Message(text='a warble', user_id=self.uid)
        db.session.add(m)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        # Message text should say "a warble"
        self.assertEqual(self.u.messages[0].text, "a warble")