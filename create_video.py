#! usr/bin/python3
# Maddix - Oct 2015 - Python 3.4

# NOTE: Not tested. Remove when it is.

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
import src.utils as utils

# TODO: Logging

def pick(folders):
	print("Pick a folder or enter 'quit' to quit. Enter a positive number.")
	count = 0
	for folder in folders:
		count += 1
		print("[{0}] {1}".format(count, folder))

	while True:
		picked = input(">> ")
		if picked == "quit" or picked == "'quit'":
			raise Exception("Bye!")
		if picked.isnumeric():
			if int(picked)-1 in range(len(folders)):
				return folders[int(picked)-1]
			else:
				print("Please pick a number form 1 to {0}.".format(len(folders)))
		else:
			print("Positive numbers only.")


if __name__ == "__main__":
	print("Loading Config.json..")
	config = utils.Handle_json("config.json", "src", [("ffmpeg-command", list)])

	print("Done.\nLocating ffmpeg.exe..")
	if not utils.check_for_ffmpeg(config):
		raise Exception("Could not find ffmpeg.exe!")

	print("Done.\nLoading video folder..")
	config.check_required([
			("folder-options", dict),
				("folder-options.source", list),
				("folder-options.destination", list),
				("folder-options.image-folder-name", str),
				("folder-options.video-folder-name", str),
			("options", dict),
				("options.image-number-total-pad", int),
				("options.image-type", str),
			("ffmpeg-command", list)
			])
	destination = os.path.join(*config.get("folder-options.destination"))
	folders = os.listdir(destination)
	working_folder = os.path.join(destination, pick(folders))
	image_folder = os.path.join(destination, working_folder, config.get("folder-options.image-folder-name"))
	video_folder = os.path.join(destination, working_folder, config.get("folder-options.video-folder-name"))

	print("Done.\nCreating video..")
	utils.Create_video(config, image_folder, video_folder)
	print("Done.")

