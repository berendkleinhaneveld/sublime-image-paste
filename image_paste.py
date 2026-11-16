"""Paste clipboard images into Markdown files (macOS).

When a paste happens in a Markdown view and the clipboard holds an image but
no text, the image is saved next to the Markdown file and a Markdown image
link is inserted at the cursor.
"""

import os
import subprocess
import time
import urllib.parse

import sublime
import sublime_plugin

SETTINGS_FILE = "ImagePaste.sublime-settings"

# AppleScript that writes the clipboard image (as PNG) to the path in argv.
# Exits with an error when the clipboard has no image data.
_SAVE_PNG_SCRIPT = """
on run argv
    set outPath to item 1 of argv
    set imgData to the clipboard as «class PNGf»
    set fh to open for access (POSIX file outPath) with write permission
    try
        set eof of fh to 0
        write imgData to fh
        close access fh
    on error errMsg
        close access fh
        error errMsg
    end try
end run
"""


def _settings():
    return sublime.load_settings(SETTINGS_FILE)


def _is_markdown(view):
    return view.match_selector(0, "text.html.markdown")


def _unique_path(folder, base, ext):
    path = os.path.join(folder, base + ext)
    counter = 1
    while os.path.exists(path):
        path = os.path.join(folder, "{}-{}{}".format(base, counter, ext))
        counter += 1
    return path


def save_clipboard_image(path):
    """Write the clipboard image to ``path`` as PNG. Returns True on success."""
    try:
        result = subprocess.run(
            ["osascript", "-e", _SAVE_PNG_SCRIPT, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("ImagePaste: osascript failed:", exc)
        return False

    ok = result.returncode == 0 and os.path.isfile(path) and os.path.getsize(path) > 0
    if not ok and os.path.exists(path):
        os.remove(path)
    return ok


class PasteMarkdownImageCommand(sublime_plugin.TextCommand):
    """Save the clipboard image next to the file and insert a link to it."""

    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name:
            sublime.status_message("ImagePaste: save the Markdown file first")
            return

        folder = os.path.dirname(file_name)
        settings = _settings()
        base = time.strftime(settings.get("filename_format", "image-%Y%m%d-%H%M%S"))
        path = _unique_path(folder, base, ".png")

        view = self.view

        def work():
            if not save_clipboard_image(path):
                sublime.status_message("ImagePaste: clipboard contains no image")
                return
            rel = os.path.relpath(path, folder).replace(os.sep, "/")
            link = "![{}]({})".format(
                settings.get("alt_text", ""), urllib.parse.quote(rel)
            )
            sublime.set_timeout(
                lambda: view.run_command("insert", {"characters": link}), 0
            )
            sublime.status_message("ImagePaste: saved " + os.path.basename(path))

        sublime.set_timeout_async(work, 0)


class ImagePasteListener(sublime_plugin.EventListener):
    """Redirect regular pastes in Markdown to the image paste command when the
    clipboard holds no text (e.g. a screenshot)."""

    def on_text_command(self, view, command_name, args):
        if command_name != "paste":
            return None
        if sublime.platform() != "osx":
            return None
        if not _settings().get("enabled", True):
            return None
        if not _is_markdown(view):
            return None
        if sublime.get_clipboard():
            return None  # Text on the clipboard: normal paste.
        return ("paste_markdown_image", {})
