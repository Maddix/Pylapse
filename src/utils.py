# Maddix - Oct 2015 - Python 3.4

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
import subprocess
import shutil
import logging
import json
import time
# time.strftime("%Y-%m-%d_%I.%M%p", time.localtime())

def check_for_ffmpeg(config, logging=None):
	""" Checks for ffmpeg.exe. Uses default path or a given one in the config.json. """
	folder = os.path.join(os.path.abspath(""), "ffmpeg", "bin")
	if config.has("ffmpeg-location"):
		folder = os.path.join(*config.get("ffmpeg-location"))
		if not os.path.isdir(folder):
			raise Exception("'{0}' does not exist!".format(folder))
	if "ffmpeg.exe" in os.listdir(folder):
		return True
	return False

class Handle_json:

	def __init__(self, file_name, file_path, required=None, logging=None):
		self.file_name = file_name
		self.file_path = file_path
		self.loaded = self.load_json(os.path.join(file_path, file_name))

		if required:
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


class Handle_folders:

	def __init__(self, config, logging=None):
		config.check_required([
			("folder-options", dict),
				("folder-options.source", str),
				("folder-options.destination", str),
				("folder-options.create-destination-if-not-exists", bool),
				("folder-options.folder-name-and-date", str),
				("folder-options.image-folder-name", str),
				("folder-options.video-folder-name", str)])

		self.source = self.create_path(config.get("folder-options.source"))
		self.destination = self.create_path(config.get("folder-options.destination"),
											config.get("folder-options.create-destination-if-not-exists"))
		self.working_folder = os.path.join(self.destination, time.strftime(config.get("folder-options.folder-name-and-date"), time.localtime()))
		self.image_folder = os.path.join(self.destination, self.working_folder, config.get("folder-options.image-folder-name"))
		self.video_folder = os.path.join(self.destination, self.working_folder, config.get("folder-options.video-folder-name"))
		self.create_folders(self.working_folder, self.image_folder, self.video_folder)

	def create_folders(self, working_folder, image_folder, video_folder):
		""" Create three folders. """
		os.mkdir(working_folder)
		os.mkdir(os.path.join(working_folder, image_folder))
		os.mkdir(os.path.join(working_folder, video_folder))

	def create_path(self, path, create=False):
		path = os.path.join(*path)
		if not os.path.exists(path):
			if create:
				os.mkdir(path)
			else:
				raise Exception("Path '{0}' does not exist!".format(path))
		return path


class Handle_images:

	def __init__(self, config, source, image_folder, delete_images=False, logging=None):
		config.check_required([
			("options.image-type", str),
			("options.image-number-total-pad", int)])

		self.copied_images = self.copy_images(source, image_folder, config.get("options.image-type"))
		self.renumber_images(self.copied_images,
							 image_folder,
							 config.get("options.image-type"),
							 config.get("options.image-number-total-pad"))
		if delete_images:
			self.delete_images_from_card(self.copied_images, source)

	def copy_images(self, source, image_folder, image_type):
		""" Copy all files from source with a specific ending to destination. """
		copied = []
		for listed_file in os.listdir(source):
			if listed_file.lower().endswith(image_type):
				shutil.copy(os.path.join(source, listed_file), image_folder)
				copied.append(listed_file)
		return copied

	def renumber_images(self, image_name_list, image_folder, image_type, total_zeros):
		""" Renumber each image. """
		image_name_list.sort()
		for number in range(len(image_name_list)):
			image_name = "{0}{1}{2}".format("0"*(total_zeros - len(str(number))), str(number), image_type)
			os.rename(os.path.join(image_folder, image_name_list[number]), os.path.join(image_folder, image_name))

	def delete_images_from_card(self, copied_images, source):
		""" WARNING! Be very sure what you are doing! This can wipe files from your drive.
			Clears the images from the SD card once they have been copied to the PC.
		"""
		for copied_image in copied_images:
			os.remove(os.path.join(source, copied_image))


class Create_video:

	def __init__(self, config, image_folder, video_folder, logging=None):
		""" Create a video. """
		self.launch_ffmpeg_command(self.build_ffmpeg_command(config, image_folder, video_folder))

	def add_quotes(self, path):
		""" Surround a string in quotes. """
		return '"{0}"'.format(path)

	def build_ffmpeg_command(self, config, image_folder, video_folder):
		""" Add file paths and format ffmpeg-command string. """
		command = config.get("ffmpeg-command")
		# Path to ffmpeg.exe
		command.insert(0, self.add_quotes(os.path.join(os.path.abspath(""), "ffmpeg", "bin", command.pop(0))))
		# Input image
		index_of_input = command.index("-i")
		if index_of_input is not -1:
			input_with_path = self.add_quotes(os.path.join(image_folder, command.pop(index_of_input+1)))
			command.insert(index_of_input+1, input_with_path)
		# Output video
		command.append(self.add_quotes(os.path.join(video_folder, command.pop(-1))))
		options = config.get("options")
		output_name = "video-output-name"
		options[output_name] = time.strftime(options[output_name], time.localtime())
		return " ".join(command).format(**options)

	def launch_ffmpeg_command(self, built_command):
		""" Launch FFmpeg with the built command. """
		subprocess.call(built_command)
