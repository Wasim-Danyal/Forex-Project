import unittest

from flask import url_for
from flask_testing import TestCase

from application import app, db, bcrypt
from application.models import Users, Rates
from os import getenv

class TestBase(TestCase):

	def create_app(self):

		# pass in configurations for test database
		config_name = 'testing'
		app.config.update(SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:1234@35.246.73.168/TestBase',
				SECRET_KEY=getenv('TEST_SECRET_KEY'),
				WTF_CSRF_ENABLED=False,
				DEBUG=True
				)
		return app

	def setUp(self):
		"""
		Will be called before every test
		"""
		# ensure there is no data in the test database when the test starts
		db.session.commit()
		db.drop_all()
		db.create_all()

		# create test admin user
		hashed_pw = bcrypt.generate_password_hash('admin2016')
		admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password=hashed_pw)

		# create test non-admin user
		hashed_pw_2 = bcrypt.generate_password_hash('test2016')
		employee = Users(first_name="test", last_name="user", email="test@user.com", password=hashed_pw_2)

		# save users to database
		db.session.add(admin)
		db.session.add(employee)
		db.session.commit()

	def tearDown(self):
		"""
		Will be called after every test
		"""

		db.session.remove()
		db.drop_all()
	

class TestViews(TestBase):
	# testing to see if code 200 is returned upon access to url

	def test_homepage_view(self):
		response = self.client.get(url_for('home'))
		self.assertEqual(response.status_code, 200)
	

	def test_about_view(self):

		response = self.client.get(url_for('about'))
		self.assertEqual(response.status_code, 200)


class TestNewRate(TestBase):

	def test_add_new_rate(self):
		with self.client:
			response = self.client.post(
				'/newrate',
				data=dict(
					base_Currency="EUR",
					new_Currency="GBP",
					bid_rate="1.234",
					ask_rate="4.567"
				),
				follow_redirects=True
			)
			self.assertIn(b'EUR', response.data)

class TestUserFunctionality(TestBase):

	def test_registeruser(self):
		with self.client:
			response = self.client.post(
				'/register',
				data=dict(
					first_name="Joe",
					last_name="Bloggs",
					email="joebloggs@gmail.com",
					password="password123",
					confirm_password="password123"
				),
				follow_redirects=True
			)
			self.assertTrue(response.status_code, 200)

	def test_loginuser(self):
		with self.client:
			response = self.client.post(
				'/login',
				data=dict(
					email="joebloggs@gmail.com",
					password="password123"
				),
				follow_redirects=True
			)
			self.assertEqual(current_user.username, "admin")

	def test_logout(self):
		with self.client:
			response = self.client.get(
				'/logout',
				follow_redirects=True
			)
			self.assertFalse(current_user.is_authenticated)
		