import subprocess
from datetime import datetime
from pathlib import Path

import sublime
import sublime_plugin


def plugin_loaded():
    """
    Hook that is called by Sublime when plugin is loaded.
    """
    pass


def plugin_unloaded():
    """
    Hook that is called by Sublime when plugin is unloaded.
    """
    for key in list(globals().keys()):
        if "imagepaste" in key.lower():
            del globals()[key]


class ImagePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("image-paste.sublime-settings")
        variables = self.view.window().extract_variables()

        now = datetime.now()
        almost_now = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
        )
        name = almost_now.isoformat().replace(":", "-").replace("T", "-")

        destination_folder = Path(
            sublime.expand_variables(settings.get("folder"), variables)
        )
        if not destination_folder.is_dir():
            print(
                "Could not paste image: "
                "destination is not a folder: {}".format(destination_folder)
            )
            return

        destination = destination_folder / "{}{}.{}".format(
            settings.get("name_prefix"), name, settings.get("name_suffix")
        )

        command = ["pngpaste", str(destination)]

        file = Path(variables.get("file_path"))
        relative_path = destination.relative_to(file)
        text_to_insert = "{}{}{}".format(
            settings.get("paste_prefix"),
            str(relative_path),
            settings.get("paste_suffix"),
        )

        try:
            subprocess.check_output(command)
            for region in self.view.sel():
                self.view.insert(edit, region.begin(), text_to_insert)
        except subprocess.CalledProcessError:
            print("Paste failed. Was there no image in the clipboard?")
