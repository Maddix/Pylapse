#Json configuration

`Config.json` is split into two parts. Folder configuration and video configuration.

##Folder Configuration
You'll see these properties under `folder-options`.
* source
* destination
* create-destination-if-not-exists
* file-name-and-date
* image-folder-name
* video-folder-name

###Source and Destination

Both `source` and `destination` should be a list of strings containing a complete path to a folder. On windows the first string should be a lowercase drive letter followed by a colon `:`. On linux the first string should be a forward slash `/`. `source` should be the folder that contains your target images and `destination` should be the working directory that will contain projects.

If you run pylapse for the first time and haven't created the path for `destination`, pylapse will consult `create-destination-if-not-exists` on creating the path. I recommend you leave it as `true`.

###Project Folder Name
`folder-name-and-date` will be the name for all project folders. To keep each folder unique you can add <a href=https://docs.python.org/2/library/time.html#time.strftime>key codes</a> into the name to get the time and date.

###Image and Video folder names
`image-folder-name` and `video-folder-name` will set the generated folder names respectively. `image-folder-name` will hold processed images and `video-folder-name` will hold created videos.

####Example folder configuration
* `source`: `["d:", "pylapseImages"]` or `["/", "pylapseImages"]`.
* `destination`: `["d:", "pylapse_projects"]` or `["/", "home", "user", "pylapse_projects"]`
* `file-name-and-date`: `"%Y-%m-%d_%I.%M.%S %p"` or `"Pylapse %d %M %S %p"`
* `create-destination-if-not-exists`: `true`
* `image-folder-name`; `"images"`
* `video-folder-name`: `"videos"`

##Video Configuration

Both `options` and `ffmpeg-command` make up the configuration for video creation.

###Options

Unlike `folder-options`, pylapse only requires a few properties from `options`.
* image-number-total-pad
* image-name
* image-type
* video-output-name

Any remaining properties are used in `ffmpeg-command`.

`image-number-total-pad` sets how many `0`s are added to image names when they are copied.
`image-name` helps ffmpeg find the correct images. It should match
`iamge-type` should be a string and should be the image format of your images. Pylapse will only copy images with this type.
`video-output-name`

####Example option configuration

* `image-number-total-pad`: `5`
* `image-name`: `"%05d"
* `image-type`: `".jpeg"` or `".png"`
* `video-output-name`: `"%m-%d_%I.%M_timelapse"`

###FFmpeg-command

`ffmpeg-command` holds all the commands that will be given to ffmpeg when pylapse kicks it off. Pylapse will match commands from `options` that are inside open `{` and close `}` brackets. Such as `{video-name}` or `{image-name}`.

