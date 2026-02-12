#!/usr/bin/python3
""" ""
slast — the slightly less annoying screenshot tool
"""

import sys
import subprocess
import os
from datetime import datetime
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio, GLib


class SlastWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("slast")
        self.set_default_size(400, 200)
        self._build_ui()

    def _build_ui(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Header stuff
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="slast"))
        box.append(header)

        #  Content box for boxing contents obviously
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_valign(Gtk.Align.CENTER)
        content_box.set_halign(Gtk.Align.CENTER)
        content_box.set_vexpand(True)

        # Region capture
        region_button = Gtk.Button(label="Capture Region")
        region_button.add_css_class("pill")
        region_button.set_size_request(200, -1)
        region_button.connect("clicked", self._on_region_clicked)

        # Fullscreen Capture
        fullscreen_button = Gtk.Button(label="Capture Fullscreen")
        fullscreen_button.add_css_class("pill")
        fullscreen_button.set_size_request(200, -1)
        fullscreen_button.connect("clicked", self._on_fullscreen_clicked)

        content_box.append(region_button)
        content_box.append(fullscreen_button)

        box.append(content_box)
        self.set_content(box)

    def _on_region_clicked(self, button):
        print("Region capture requested")
        self._capture_region()

    def _on_fullscreen_clicked(self, button):
        print("Fullscreen capture requested")
        self._capture_fullscreen()

    def _capture_region(self):
        """Capture a selected region using slurp and grim"""
        try:
            # Hide window to get it out of the way
            self.set_visible(False)
            GLib.timeout_add(100, self._do_region_capture)
        except Exception as e:
            print(f"Error initiating region capture: {e}")
            self.set_visible(True)

    def _do_region_capture(self):
        """Actually perform the region capture after window is hidden"""
        try:
            # Use slurp to select region
            result = subprocess.run(
                ["slurp"], capture_output=True, text=True, check=True
            )
            region = result.stdout.strip()

            if region:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.expanduser(f"~/Pictures/screenshot_{timestamp}.png")

                # Capture with grim
                subprocess.run(["grim", "-g", region, filename], check=True)
                print(f"Screenshot saved to {filename}")

                # Copy to clipboard
                subprocess.run(
                    ["wl-copy", "--type", "image/png"],
                    stdin=open(filename, "rb"),
                    check=False,
                )
        except subprocess.CalledProcessError:
            print("Region capture cancelled or failed")
        except Exception as e:
            print(f"Error during region capture: {e}")
        finally:
            self.set_visible(True)

        return False  # Don't repeat the timeout

    def _capture_fullscreen(self):
        """Capture the entire screen using grim"""
        try:
            # Hide window
            self.set_visible(False)
            GLib.timeout_add(100, self._do_fullscreen_capture)
        except Exception as e:
            print(f"Error initiating fullscreen capture: {e}")
            self.set_visible(True)

    def _do_fullscreen_capture(self):
        """Actually perform the fullscreen capture after window is hidden"""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.expanduser(f"~/Pictures/screenshot_{timestamp}.png")

            # Capture with grim
            subprocess.run(["grim", filename], check=True)
            print(f"Screenshot saved to {filename}")

            # Copy to clipboard
            subprocess.run(
                ["wl-copy", "--type", "image/png"],
                stdin=open(filename, "rb"),
                check=False,
            )
        except Exception as e:
            print(f"Error during fullscreen capture: {e}")
        finally:
            self.set_visible(True)

        return False  # Don't repeat the timeout


class SlastApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="io.github.slast", flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = SlastWindow(application=self)

        self.window.present()


def main():
    app = SlastApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
