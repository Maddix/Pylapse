# Maddix - Oct 2015

"""
The MIT License (MIT)

Copyright (c) 2015 Maddix

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
from os.path import join as os_join


class Handle_json:

	def __init__(self, file_name, file_path, required):
		self.file_name = file_name
		self.file_path = file_path
		self.loaded = self.load_json(os_join(file_path, file_name))
		self.required = required
		self.check_required(required)

	def get(self, connected_string):
		""" Return item else False.
			connected_string -> "foo.fighters.favorite_snack" """
		path_value = self.loaded
		for item in connected_string.split("."):
				path_value = path_value.get(item)
				if path_value is None:
					return False
		return path_value

	def has(self, connected_string):
		""" Returns a bool.
			connected_string -> "foo.fighters.favorite_snack" """
		if self.get(connected_string):
			return True
		return False

	def check_required(self, required):
		""" Checks the loaded json for required items.
			required -> [("foo.fighters.snack", type), ..] """
		for pair in required:
			if not self.has(pair[0]) and type(self.get(pair[0])) is not pair[1]:
				raise Exception("Config file doesn't have '{0}' or it isn't the required type of '{1}'.".format(*pair))

	def check_list(self, unchecked_list, typeList):
		""" Validates items in 'unchecked_list' with items in 'typeList'. 'typeList' must contain valid
			types and have at least one type.
			- unchecked_list -> ["one", "two", 3, "four", "five", 6]
			- typeList -> [str, str, int]
			- returns uncheck_list """
		count = 0
		for item in unchecked_list:
			valid_type = typeList[count%len(typeList)]
			if type(item) is not valid_type:
				raise Exception("'{0}' failed validation. '{1}' should be '{2}'.".format(unchecked_list, item, valid_type))
			count += 1
		return unchecked_list

	def load_json(self, location_file_name):
		""" Load the file into python objects """
		loaded_json = None
		with open(location_file_name, "r") as open_file:
			loaded_json = json.load(open_file)
		return loaded_json
