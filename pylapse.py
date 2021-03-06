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

import src.utils as utils

# TODO: Logging

if __name__ == "__main__":
	print("Loading Config.json..")
	config = utils.Handle_json("config.json", "src", [("ffmpeg-command", list)])
	print("Done.\nCreating folders..")
	folders = utils.Handle_folders(config)
	print("Done.\nCopying images..")
	images = utils.Handle_images(config, folders.source, folders.image_folder)
	print("Done.\nLocating ffmpeg.exe..")
	if not utils.check_for_ffmpeg(config):
		raise Exception("Could not find ffmpeg.exe!")
	print("Done.\nCreating video..")
	video = utils.Create_video(config, folders.image_folder, folders.video_folder)
	print("Done.")

