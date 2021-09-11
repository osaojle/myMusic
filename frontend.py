import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from mutagen.mp3 import MP3
import os, time, fnmatch, alsaaudio
from audioplayer import AudioPlayer
wait = time.sleep

def main():
    style_provider = Gtk.CssProvider()

    css = open(('./style.css'), 'rb') # rb needed for python 3 support
    css_data = css.read()
    css.close()

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


    title = "Oh The Nostalgia"

    window = Gtk.Window(title=title)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    window.add(box)
    anotherheader = Gtk.HeaderBar()
    window.add(anotherheader)
    boxright = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

    def flscr(e):
        window.fullscreen()

    def unfl(widget, ev):
        if ev.keyval == Gdk.KEY_Escape:
            window.unfullscreen()

    def headerr():
        search=Gtk.SearchEntry()
        fullscreen=Gtk.Button(label="Party Mode")
        fullscreen.connect("clicked", flscr)
        titlehb = Gtk.Label(label=title)
        header_bar = Gtk.HeaderBar(spacing=15)
        header_bar.set_show_close_button(True)
        window.set_titlebar(header_bar)

        def srch(widget):
            print(search.get_text())

        search.connect('activate', srch)

        def pack():
            header_bar.pack_start(titlehb)
            header_bar.pack_end(fullscreen)
            header_bar.set_custom_title(search)
        pack()

    headerr()

    result = []
    def find(pattern, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root,name))
        return result

    find('*.mp3', '../')
    for i in result:
        player = AudioPlayer(i)
        player.play()
        audio = MP3(i)
        audio_info = audio.info
        length_in_secs = int(audio_info.length)
    player.pause()


    def playmain():
        # song = AudioSegment.from_mp3("../BetterDays.mp3")
        # # play(song)
        # audio = MP3("../BetterDays.mp3")
        # # Contains all the metadata about the mp3 file
        # # audio_info = audio.info
        # length_in_secs = int(audio_info.length)
        currentbar=Gtk.Scale().new_with_range(Gtk.Orientation.HORIZONTAL,2,length_in_secs,1)
        currentbar.set_sensitive(False)

        volcontrol=Gtk.VolumeButton()
        playbtn=Gtk.ToggleButton(label="▸")

        stopbtn=Gtk.Button(label="×")
        vis=Gtk.Button(label="~")

        def update_progressbar():
            currentpos=currentbar.get_value()
            currentpos+=1
            if currentpos<=length_in_secs:
                currentbar.set_value(currentpos)
            else:
                currentbar.set_value(0.0)
            return True
            # currentbar.set_max_value(length_in_secs)

        mixer = alsaaudio.Mixer()
        def changevol(widget, value):
            mixer.setvolume(int(value*100))

        volcontrol.connect("value-changed", changevol)
        idloop=None
        def playornot(widget):
            global idloop
            if playbtn.get_active() == True:
                idloop=GLib.timeout_add(1000, update_progressbar)
                playunpausemusic()
            else:
                GLib.source_remove(idloop)
                playmusicpause()

        def playmusicpause():
            playbtn.set_label("▸")
            player.pause()

        def playunpausemusic():
            playbtn.set_label("| |")
            player.resume()

        playbtn.connect("toggled", playornot)

        def stopfunc(widget):
            global idloop
            GLib.source_remove(idloop)
            playbtn.set_active(False)
            player.stop()

        def visfunc(widget):
            return True
        stopbtn.connect("clicked", stopfunc)
        vis.connect("clicked", visfunc)

        def packappend():
            box.add(anotherheader)
            box.add(currentbar)
            boxright.add(stopbtn)
            boxright.add(playbtn)
            boxright.add(vis)
            boxright.add(volcontrol)
            anotherheader.set_custom_title(boxright)

        packappend()
    playmain()


    window.connect('key_release_event', unfl)
    window.maximize()
    window.connect('destroy', exit)
    style_provider.load_from_data(css_data)
    window.show_all()
    Gtk.main()

main()
