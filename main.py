#! usr/bin/python3
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
import time
# time.strftime("%Y-%m-%d_%I.%M%p", time.localtime())
import src.json_parser as parser


class Handle_images():

	def __init__(self, config):
		self.source = self.create_path(config.get("folder-options.source"))
		self.destination = self.create_path(config.get("folder-options.destination"),
											config.get("folder-options.create-destination-if-not-exists"))
		self.working_folder = os.path.join(self.destination, time.strftime(config.get("folder-options.file-name-and-date"), time.localtime()))
		self.image_folder = os.path.join(self.destination, self.working_folder, config.get("folder-options.image-folder-name"))
		self.video_folder = os.path.join(self.destination, self.working_folder, config.get("folder-options.video-folder-name"))
		self.create_folders(self.working_folder, self.image_folder, self.video_folder)
		self.copied_images = self.copy_images(self.source, self.image_folder, config.get("options.image-type"))
		self.renumber_images(self.copied_images,
							 self.image_folder,
							 config.get("options.image-type"),
							 config.get("options.image-number-total-pad"))
		#self.delete_images_from_card(self.copied_images, self.source)

	def create_folders(self, working_folder, image_folder, video_folder):
		""" Create three folders. """
		os.mkdir(working_folder)
		os.mkdir(os.path.join(working_folder, image_folder))
		os.mkdir(os.path.join(working_folder, video_folder))

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

	def create_path(self, path, create=False):
		path = os.path.join(*path)
		if not os.path.exists(path):
			if create:
				os.mkdir(path)
			else:
				raise Exception("Path '{0}' does not exist!".format(path))
		return path


class Main():

	def __init__(self):
		self.config_name = "config.json"
		self.config_path = "src"
		self.required_from_config = [
			("folder-options", dict),
				("folder-options.source", str),
				("folder-options.destination", str),
				("folder-options.create-destination-if-not-exists", bool),
				("folder-options.file-name-and-date", str),
				("folder-options.image-folder-name", str),
				("folder-options.video-folder-name", str),
			("options", dict),
				("options.image-number-total-pad", int),
				("options.image-name", str),
				("options.image-type", str),
				("options.image-per-second", int),
				("options.image-start-number", int),
				("options.video-framerate", int),
				("options.video-codec", str),
				("options.video-height", int),
				("options.video-width", int),
				("options.video-output-name", str),
				("options.video-container", str),
			("ffmpeg-command", list)
		]
		self.config = parser.Handle_json(self.config_name, self.config_path, self.required_from_config)
		self.handle_images = Handle_images(self.config)

		print(self.build_ffmpeg_command(self.config, self.handle_images))

	def build_ffmpeg_command(self, config, handle_images):
		""" Add file paths and format ffmpeg-command string. """
		command = config.get("ffmpeg-command")
		index_of_input = command.index("-i")
		# Input image
		if index_of_input is not -1:
			input_with_path = os.path.join(handle_images.image_folder, command.pop(index_of_input+1))
			command.insert(index_of_input+1, input_with_path)
		# Output video
		command.append(os.path.join(handle_images.video_folder, command.pop(-1)))
		return " ".join(command).format(**config.get("options"))

	def launch_ffmpeg_command(self, built_command):
		pass

if __name__ == "__main__":
	Main()
	input("Enter to close.")

