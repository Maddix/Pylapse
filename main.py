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
import shutil
import time
# time.strftime("%Y-%m-%d_%I.%M%p", time.localtime())
import src.json_parser as parser


class Parse_config(parser.Parse_json):

	def __init__(self, config_file_name):

		self.copy = False
		self.source = []
		self.destination = []
		self.file_name_and_date = ""
		self.create_destination = False
		self.copy_files_with_ending = ""
		self.ffmpeg_options = {}

		self.config_file_name = config_file_name
		self.loaded_config = self.load_json(config_file_name)
		self.parse_config(self.loaded_config)

	def parse_config(self, loaded_config):
		self.copy = self.check_property(loaded_config, "config", "copy", bool)
		self.source = self.check_property(loaded_config, "config", "source", list)
		self.destination = self.check_property(loaded_config, "config", "destination", list)
		self.create_destination = self.check_property(loaded_config, "config", "create-destination-if-not-exists", bool)
		self.copy_files_with_ending = self.check_property(loaded_config, "config", "copy-files-with-ending", str)
		self.file_name_and_date = self.check_property(loaded_config, "config", "file-name-and-date", str)
		self.ffmpeg_options = self.check_property(loaded_config, "config", "ffmpeg-options", dict)


class Copy_images():

	def __init__(self, source, destination, create_destination, file_name_and_date, copy_files_with_ending):
		self.source = self.create_path(source)
		self.destination = self.create_path(destination, create_destination)
		self.copy_files_with_ending = copy_files_with_ending
		self.working_folder = os.path.join(self.destination, time.strftime(file_name_and_date, time.localtime()))
		self.image_folder = "images"
		self.video_folder = "video"


		self.create_folders()
		self.copied_images = self.copy_images()
		#self.delete_images_from_card()

	def create_folders(self):
		""" Create three folders. """
		os.mkdir(self.working_folder)
		os.mkdir(os.path.join(self.working_folder, self.image_folder))
		os.mkdir(os.path.join(self.working_folder, self.video_folder))

	def copy_images(self):
		""" Copy all files from source with a specific ending to destination. """
		copied = []
		for listed_file in os.listdir(self.source):
			if listed_file.lower().endswith(self.copy_files_with_ending):
				shutil.copy(os.path.join(self.source, listed_file),
							os.path.join(self.destination, self.working_folder, self.image_folder))
				print(listed_file)
				copied.append(listed_file)
		return copied

	def delete_images_from_card(self):
		""" WARNING! Be very sure what you are doing! This can wipe files from your drive.
			Clears the images from the SD card once they have been copied to the PC.
		"""
		for copied_image in self.copied_images:
			os.remove(os.path.join(self.source, copied_image))

	def create_path(self, path, create=False):
		path = os.path.join(*path)
		if not os.path.exists(path):
			if create:
				os.mkdir(path)
			else:
				raise Exception("Path '{0}' does not exist!".format(path))
		return path

if __name__ == "__main__":
	config = os.path.join("src", "config.json")
	parse = Parse_config(config)
	print(parse)
	copy = Copy_images(parse.source, parse.destination, parse.create_destination, parse.file_name_and_date, parse.copy_files_with_ending)
	print(copy)


	input("Enter to close.")

