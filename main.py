#! usr/bin/python3
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

import os
import time
# time.strftime("Timelapse %Y-%m-%d@%H-%M", time.gmtime())
import src.json_parser as parser


class parse_config(parser.Parse_json):

	def __init__(self, config_file_name):
		self.config_file_name = config_file_name
		self.loaded_config = self.load_json(config_file_name)
		self.parse_config(self.loaded_config)

		self.copy = False
		self.copy_from = []
		self.copy_to = []
		self.ffmpeg_options = {}

	def parse_config(self, loaded_config):
		self.copy = self.check_property(loaded_config, "config", "copy", bool)
		self.copy_from = self.check_property(loaded_config, "config", "copy-from", list)
		self.copy_to = self.check_property(loaded_config, "config", "copy-to", list)
		self.date_format = self.check_property(loaded_config, "config", "date-format", str)
		self.ffmpeg_options = self.check_property(loaded_config, "config", "ffmpeg-options", dict)


class copy_images():

	def __init__(self, copy_from, copy_to):
		self.copy_from = self.create_path(copy_from)
		self.copy_to = self.create_path(copy_to)

	def create_folders(self):
		pass

	def delete_images_from_card(self):
		""" WARNING! Be very sure what you are doing! This can wipe files from your drive.
			Clears the images from the SD card once they have been copied to the PC.
		"""
		pass

	def create_path(self, path):
		path = os.path.join(*path)
		if not os.path.exists(path):
			raise Exception("Path '{0}' does not exist!".format(path))
		return path

	def copy_images(self):


if __name__ == "__main__":
	print(parser.Parse_json)
	input("Enter to close.")

