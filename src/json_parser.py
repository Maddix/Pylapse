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

class Parse_json:

	def check_error(self, item, msg):
		""" If item is None or False raise error with msg otherwise return item. """
		if item is None or item is False:
			raise Exception(msg)
		return item

	def check_type(self, item, requested_item_type, item_property):
		""" If item isn't the requested_item_type then throw an error otherwise return item. """
		if type(item) is not requested_item_type:
			raise Exception("'{0}' should be of type '{1}' for property '{2}'.".format(item, requested_item_type, item_property))
		return item

	def check_property(self, dictionary, parent_property_name, property_name, required_type):
		""" Checks to see if a property exists on a dictionary. """
		return self.check_type(self.check_error(dictionary.get(property_name), "'{0}' requires property '{1}'.".format(parent_property_name, property_name)), required_type, property_name)

	def check_require(self, dictionary, properties_list, require_all=False):
		""" Checks 'dictionary' for items in 'properties_types_list' and checks type. Throw error is all are missing.
			'properties_list' must be a list. """
		failed = []
		for key in properties_types_list:
			property_name = properties_list[key][0]
			if not dictionary.get(property_name):
				failed.append(property_name)
		if require_all and failed:
			raise Exception("Expected at least one property. Could not find {0}.".format(" or ".join(failed)))
		return dictionary


	def check_list(self, unchecked_list, typeList):
		""" Validates items in 'unchecked_list' with items in 'typeList'. 'typeList' must contain valid
		types and have at least one type.

		unchecked_list -> ["one", "two", 3, "four", "five", 6]
		typeList -> [str, str, int]

		returns uncheck_list

		"""
		count = 0
		for item in unchecked_list:
			valid_type = typeList[count%len(typeList)]
			if type(item) is not valid_type:
				raise Exception("'{0}' list failed validation. '{1}' should be '{2}'.".format(unchecked_list, item, valid_type))
			count += 1
		return unchecked_list

	def load_json(self, location_file_name):
		""" Load the file into python objects """
		loaded_json = None
		with open(location_file_name, "r") as open_file:
			loaded_json = json.load(open_file)
		return loaded_json
