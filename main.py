#!/usr/bin/python3
"""""
slast — the slightly less annoying screenshot tool
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

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
    
    def _on_fullscreen_clicked(self, button):
        print("Fullscreen capture requested")


class SlastApplication(Adw.Application):    
    def __init__(self):
        super().__init__(
            application_id="io.github.slast",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
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