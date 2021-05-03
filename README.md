# Image Paste

Sublime Text plugin for pasting images from the clipboard. Utilizes the
[pngpaste](https://github.com/jcsalterego/pngpaste) utility for the pasting
functionality, because the clipboard within Sublime only supports strings:
no binary data. So that's why this plugin is currently macOS only.

## Usage

Use the command: 'image-paste: Paste image' (Default key-binding set to
CMD+OPTION+V) to paste the image. Use the settings to adjust the destination
and the string that will be inserted into the text.
Make sure that the folder into which you've configured the plugin to
paste the image already exists.

## Settings

Use the `folder` setting to configure where to store the image.
`${folder}` will be substituted with the currently opened folder.
`${file_path}` will be substituted with the folder that contains
the currently opened file (default setting).
Use the `paste_prefix` and `paste_suffix` settings to specify a prefix
and a suffix for the text that will be inserted into the current view.

Valid values for `name_suffix` are: `png`, `gif`, `jpeg` and `tiff`,
which determines the output format.

## Prerequisites

`pngpaste` needs to be installed:

```sh
brew install pngpaste
```
