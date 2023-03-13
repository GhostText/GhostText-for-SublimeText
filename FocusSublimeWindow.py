import os
import sublime
import subprocess
from sublime_plugin import WindowCommand


NATIVE_FOCUS_WINDOW = int(sublime.version()) >= 4067


class FocusSublimeWindowCommand(WindowCommand):
    """
    Focuses the SublimeText window.
    """
    def run(self, **args):
        if NATIVE_FOCUS_WINDOW:
            self.window.bring_to_front()

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
        elif platform == 'windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                'powershell -Command (New-Object -ComObject WScript.Shell).AppActivate({})'
                .format(os.getppid()),
                startupinfo=startupinfo
            )
