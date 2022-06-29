from tkinter import filedialog, ttk, IntVar, Canvas, DISABLED, ACTIVE, NORMAL, NW
from image_handler import ImageHandler


class WaterMarkGUI():
    def __init__(self, window):
        """class for a gui that watermarks images"""
        self.window = window
        self.image_handler = ImageHandler()

    def load_gui(self):
        """creates all the widgets used in the gui"""
        self.window.geometry("500x650")
        self.window.title('Watermark')
        self.text_label = ttk.Label(
            text='Add a watermark to any image!').pack(side='top')
        self.size_label = ttk.Label(text='watermark size')
        self.upload_button = ttk.Button(
            text="Upload Image", command=self.upload_image)
        self.save_button = ttk.Button(
            text="Save New Image", command=self.save_image)
        self.retry_button = ttk.Button(
            text="Try Again", command=self.reload_gui)
        self.watermark_image_button = ttk.Button(
            text="Upload Watermark", command=self.select_image_watermark)
        self.watermark_text_entry = ttk.Entry()
        self.slider = ttk.Scale(self.window, from_=1, to=10, orient='horizontal')
        self.slider.set(1)
        self.text_var = IntVar()
        self.image_var = IntVar()
        self.confirm_var = IntVar()
        self.text_mark_cb = ttk.Checkbutton(
            self.window, text='Add text watermark',variable=self.text_var, command=self.watermark_selector)
        self.image_mark_cb = ttk.Checkbutton(
            self.window, text='Add image watermark',variable=self.image_var, command=self.watermark_selector)
        self.confirm_cb = ttk.Checkbutton(
            self.window, text='Confirm',variable=self.confirm_var, command=self.watermark_confirmed)
        self.canvas = Canvas(
            self.window, width = 300, height = 300) 
        self.img_path = "" 
        self.watermark_path = "" 
        self.text_mark_cb.pack()
        self.image_mark_cb.pack()
        

    def reload_gui(self):
        """loads the gui in the same state as when first opened"""
        for widget in self.window.winfo_children():
            widget.destroy()
        self.load_gui()

    def watermark_selector(self):
        """displays/hides the widgets for adding either text or image watermarks, depending on if the 
        text or image checkbox is selected"""
        if self.text_var.get():
            self.image_mark_cb.config(state=DISABLED)
            self.watermark_text_entry.pack()
        else:
            self.image_mark_cb.config(state=ACTIVE)
            if self.confirm_var.get():
                self.reload_gui()
            self.watermark_text_entry.pack_forget()
            
        if self.image_var.get():
            self.text_mark_cb.config(state=DISABLED)
            self.confirm_cb.config(state=DISABLED)
            self.watermark_image_button.pack()
        else:
            self.text_mark_cb.config(state=ACTIVE)
            if self.confirm_var.get():
                self.reload_gui()
            self.watermark_image_button.pack_forget()

        if self.image_var.get() or self.text_var.get():
            self.size_label.pack()
            self.slider.pack()
            self.confirm_cb.pack()
        if not self.image_var.get() and not self.text_var.get():
            self.slider.pack_forget()
            self.size_label.pack_forget()
            self.confirm_cb.pack_forget()

           

    def watermark_confirmed(self):
        """disables/enables the text or image upload and size change widgets, depending on if the confirm
        checkbox is selected. Loads the widget for uploading the main image"""
        if self.confirm_var.get() and self.text_var.get():
            self.watermark_text_entry.config(state=DISABLED)
            self.slider.config(state=DISABLED)
        else:
            self.watermark_text_entry.config(state=NORMAL)
            self.slider.config(state=ACTIVE)

        if self.confirm_var.get() and self.image_var.get():
            self.watermark_image_button.config(state=DISABLED)
            self.slider.config(state=DISABLED)
        else:
            self.watermark_image_button.config(state=ACTIVE)
            self.slider.config(state=ACTIVE)

        if self.confirm_var.get():
            self.upload_button.pack(side='top')
            self.canvas.pack()
        else:
            self.upload_button.pack_forget()
            self.canvas.pack_forget()


    def select_image_watermark(self):
        """opens the file system to select a image to be used as a watermark, adds it to the image handler"""
        self.watermark_path = filedialog.askopenfilename(initialdir='/Downloads', title='Select Photo',
                                          filetypes=(('JPEG files', '*.jpg'),))
        self.image_handler.watermark_image(self.watermark_path)
        self.confirm_cb.config(state=ACTIVE)
        

    def upload_image(self):
        """opens the image to watermark, adds the watermark using the image handler, displays the watermarked image"""
        self.img_path = filedialog.askopenfilename(initialdir='/Downloads', title='Select Photo',
                                          filetypes=(('JPEG files', '*.jpg'),))
        self.image_handler.main_image(self.img_path)
        if self.confirm_var.get() and self.text_var.get():
            self.image_handler.add_text_watermark(
                text=self.watermark_text_entry.get(), size=self.slider.get())
            self.preview_display()
        if self.confirm_var.get() and self.image_var.get():
            self.image_handler.add_image_watermark(size=self.slider.get())
            self.preview_display()

    def preview_display(self):
        """displays the image in the gui, disables all previous widgets and enables the save and retry button widgets"""
        self.resized_image = self.image_handler.resize_image()
        self.canvas.create_image(20, 20, anchor=NW, image=self.resized_image) 
        self.canvas.image = self.image_handler.main_img
        for widget in self.window.winfo_children():
            try:
                widget.config(state=DISABLED)
            except:
                continue
        self.save_button.config(state=ACTIVE)
        self.retry_button.config(state=ACTIVE)
        self.save_button.pack(side='left')
        self.retry_button.pack(side='right')

    def save_image(self):
        """saves the watermarked image"""
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename:
            return self.image_handler.save_image(filename)
