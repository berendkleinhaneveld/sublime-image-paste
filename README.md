# Image Paste

Sublime Text plugin for pasting images. Utilizes the `pngpaste` utility
for the pasting functionality, because the clipboard within Sublime only
supports strings: no binary data. And therefore it is currently macOS
only.

## Usage

Use the command: 'image-paste: Paste image' to paste the image. Use the
settings to adjust the destination and the string that will be inserted
into the text.
Make sure that the folder into which you've configured the plugin to
paste the image already exists.

## Settings

Use the `folder` settings to configure where to store the image.
`${folder}` will be substituted with the currently opened folder.
`${file_path}` will be substituted with the folder that contains
the currently opened file.

## Prerequisites

`pngpaste` needs to be installed:

```sh
brew install pngpaste
```
