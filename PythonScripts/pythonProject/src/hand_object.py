import json


class HandPoint:
	def __init__(self, id, x, y, z):
		self.id = id
		self.x = x
		self.y = y
		self.z = z


class HandPointEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__
