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

def pick(folders, msg):
	for number, folder in range(1, len(folders)), folders:
		print("[{0}] {1}".format(number, folder))
	print("(Enter 'quit' to exit.)")

	while True:
		picked = input(msg)
		if picked is "quit" or picked is "'quit'":
			raise Exception("Bye!")
		if picked.isnumeric() and -1 < picked <= len(folders):
			return folders[picked]


if __name__ == "__main__":
	print("Loading Config.json..")
	config = utils.Handle_json("config.json", "src", [("ffmpeg-command", list)])

	print("Done.\nLoading video folder..")
	config.check_require([
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
	msg = "Create video from project. Pick {0} to {1}".format(min(0, len(choices)), len(choices))
	working_folder = os.path.join(destination, pick(folders, msg))
	image_folder = os.path.join(destination, working_folder, config.get("folder-options.image-folder-name"))
	video_folder = os.path.join(destination, working_folder, config.get("folder-options.video-folder-name"))

	print("Done.\nCreating video..")
	utils.Create_video(config, image_folder, video_folder)
	print("Done.")

