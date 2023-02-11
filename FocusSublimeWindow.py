import os
import sublime
import subprocess
from sublime_plugin import WindowCommand


NATIVE_FOCUS_WINDOW = int(sublime.version()) >= 4000


class FocusSublimeWindowCommand(WindowCommand):
    """
    Focuses the SublimeText window.
    """
    def run(self, **args):
        if NATIVE_FOCUS_WINDOW:
            self.window.bring_to_front()
            return

        platform = sublime.platform()
        if platform == 'linux':
            os.system('sh -c "xdotool windowactivate $(xdotool search --class sublime | tail -1)"')
        elif platform == 'osx':
            script = """
            tell application "Sublime Text"
                activate
            end tell
            """  # Brings ALL the windows forward
            subprocess.Popen(["osascript", "-e", script])
        elif platform == 'windows':  # needs http://www.nirsoft.net/utils/nircmd.html to be installed in windows dir
            subprocess.Popen('nircmd win activate process sublime_text.exe')
