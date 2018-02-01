# project/test.py

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	# executed after each test
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# individual test cases

	# 1. adding new user
	def test_user_setup(self):
		new_user = User("John", "johnsmith@js.com", "johnsmith")
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.name 
		assert t.name == "John"

	# 2. form is present
	def test_form_is_present(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please sign in to access your task list', response.data)

	# 3. unregistered users cannot log in
	def login(self, name, password):
		return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn(b'Invalid username or password.', response.data )

	# 4. registered users can log in
	def register(self, name, email, password, confirm):
		return self.app.post(
			'register/',
			data=dict(name=name, email=email, password=password, confirm=confirm),
			follow_redirects=True
			)

	def test_users_can_login(self):
		self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		response = self.login('John', 'johnsmith')
		self.assertIn(b'Welcome!', response.data)

	def test_invalid_form_data(self):
		self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		response = self.login('alert("alert box!");', 'foo')
		self.assertIn(b'Invalid username or password.', response.data)

	# 5. form is present on register page
	def test_form_is_present_on_register_page(self):
		response = self.app.get('register/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register to access the task list.', response.data)
	
	# 6. users can register (form validation)
	def test_user_registration_error(self):
		self.app.get('register/', follow_redirects=True)
		self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		self.app.get('register/', follow_redirects=True)
		response = self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		self.assertIn(b'The username and/or email already exist.', response.data)

	# 7. users can log out
	def logout(self):
		return self.app.get('logout/', follow_redirects=True)

	def test_logged_in_users_can_logout(self):
		self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		self.login('John', 'johnsmith')
		response = self.logout()
		self.assertIn(b'Goodbye!', response.data)

	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		self.assertNotIn(b'Goodbye!', response.data)

	# 8. users can access tasks page
	def test_logged_in_users_can_access_tasks_page(sel):
		self.register('John', 'johnsmith@js.com', 'johnsmith', 'johnsmith')
		self.login('John', 'johnsmith')
		response = self.app.get('tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Add a new task:', response.data)

	def test_not_logged_in_users_cannot_access_tasks_page(self):
		response = self.app.get('tasks/')
		self.assertIn(b'You need to login first.', response.data)

	# task helpers
	def create_user(self, name, email, password):
		new_user = User(name=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('add/', 
			data=dict(
				name='Write test cases',
				due_date='01/30/2018',
				priority='1',
				posted_date='01/30/2018',
				status='1'
				),
			follow_redirects=True)

if __name__ == "__main__":
	unittest.main()
