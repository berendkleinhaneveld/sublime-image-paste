# ImagePaste

Sublime Text plugin (macOS) for pasting images into Markdown.

Take a screenshot to the clipboard (e.g. `⌘⇧⌃4`), then press `⌘V` in a Markdown
file. The image is saved as a PNG (by default in the same folder as the
Markdown file) and a link like `![](image-20261116-142501.png)` is inserted at
the cursor.

Text pastes behave as usual: the plugin only takes over when the clipboard
holds no text. The Markdown file must be saved first so the plugin knows where
to put the image.

## Install

```sh
ln -s "$PWD" ~/Library/Application\ Support/Sublime\ Text/Packages/ImagePaste
```

## Settings

`Preferences: Image Paste Settings` from the command palette:

- `enabled` — turn the paste interception on/off
- `folder` — where to save images (default `${file_path}`, the Markdown
  file's folder). Supports Sublime variables like `${file_path}` and
  `${folder}`; relative paths are relative to the Markdown file. The folder is
  created if needed, e.g. `"${file_path}/images"`
- `filename_format` — strftime pattern for the image filename
- `alt_text` — alt text for the inserted link

## License

MIT — see [LICENSE](LICENSE).
