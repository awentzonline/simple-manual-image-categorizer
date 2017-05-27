#!/usr/bin/env python
import hashlib
import os
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from PIL import Image, ImageTk


class ImageCategorizer:
    def __init__(self, src_path, dest_root_path):
        self.src_path = src_path
        self.dest_root_path = dest_root_path
        self.setup()

    def setup(self):
        self.src_imgs = []
        # recursively gather source images
        for root, dirs, files in os.walk(self.src_path):
            self.src_imgs += [
                os.path.join(root, f) for f in files
            ]
        self.dest_paths = os.listdir(self.dest_root_path)
        # filter out non-directory paths in destination
        self.dest_paths = [
            p for p in self.dest_paths \
            if os.path.isdir(os.path.join(self.dest_root_path, p))
        ]
        self.next_image(pop=False)

    def next_image(self, pop=True):
        '''Advance to next good image.'''
        if not self.src_imgs:
            return
        self.current_image = None
        if pop:
            self.src_imgs.pop()
        # validate the image
        try:
            self.current_image = Image.open(self.current_image_path).convert('RGB')
        except IOError, e:
            print(e)
            # not good; try the next one
            print('bad image {}'.format(self.current_image_path))
            self.next_image()

    def move_current_image_to(self, category_name):
        '''Move image to category path and rename to hash of contents.'''
        src_path = self.src_imgs.pop()
        #src_path = os.path.join(self.src_path, img_name)
        current_image_hash = hashlib.md5(self.current_image.tobytes()).hexdigest()
        dest_name = '{}.jpg'.format(current_image_hash)
        dest_path = os.path.join(self.dest_root_path, category_name, dest_name)
        print('renaming {} to {}'.format(src_path, dest_path))
        os.rename(src_path, dest_path)

    @property
    def current_image_path(self):
        if not self.src_imgs:
            return None
        return self.src_imgs[-1]

    @property
    def is_complete(self):
        return not self.src_imgs


class Application(tk.Frame):
    def __init__(self, config, master=None):
        self.config = config
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.setup_categorizer()
        self.quit_button = tk.Button(
            self, text='Quit', command=self.quit)
        self.quit_button.grid()

    def display_current_image(self, max_size=(512, 512)):
        img = self.categorizer.current_image.copy()
        img.thumbnail(max_size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image=img)
        self.img_panel.configure(image=image)
        self.img_panel.image = image

    def next_image(self):
        self.categorizer.next_image()

    def setup_categorizer(self):
        self.categorizer = ImageCategorizer(self.config.src_path, self.config.dest_root_path)
        self.img_panel = tk.Label(self)
        self.display_current_image()
        self.img_panel.grid()
        def selected_category_callback(path):
            def f(*_):
                self.categorizer.move_current_image_to(path)
                self.categorizer.next_image()
                if self.categorizer.is_complete:
                    print("that's it!")
                else:
                    print(self.categorizer.current_image_path)
                    self.display_current_image()
            return f
        buttons = tk.Frame(self)
        buttons.grid()
        for i, path in enumerate(self.categorizer.dest_paths):
            on_selected_category = selected_category_callback(path)
            text = path.replace('_', ' ').title()
            button = tk.Button(
                buttons, text=text, command=on_selected_category)
            button.grid(column=i, row=0)
            # bind hotkey
            self.master.bind(str(i + 1), on_selected_category)
        #self.display_current_image()  # weird bug makes window fill screen
        self.img_panel.grid()
