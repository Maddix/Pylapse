# About

Pylapse creates time-lapse video from a collection of images with minimal interaction.

# Use

Make sure you configure <a href=https://github.com/Maddix/Pylapse/wiki/How-to-configure-config.json>config.json</a> before use.

`pylapse.py` will atempt to copy images from a given folder to a given project folder and rename them to work with FFmpeg. It will then kick off FFmpeg to create a video with settings from config.json.

If you just want to recreate a video from a project folder run `create_video.py` and it will prompt you for the project folder.

# Tools

<a href=https://github.com/FFmpeg/FFmpeg>FFmpeg</a> is used to stitch the images into a video.
