import sys
from flask_login import UserMixin

sys.path.append('./Model')

from Model import userModel

class User(UserMixin):
	def get_id(self):
		pass