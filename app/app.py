from tkinter import ttk
from threading import Thread
from turtle import width
from typing import Callable
from get_chrome_driver import GetChromeDriver
from app.utils import build_instruction
import settings
import labels
from tkinter import filedialog, messagebox
import os
import tkinter as tk
from pathlib import Path
# import tkinter.scrolledtext as tkscrolled


class Application(tk.Frame):

    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.pack(fill=tk.X, padx=10, pady=10)
        self.__create_variables(master)
        self.__create_widgets()

    def __create_variables(self, master):
        """
        Creates the variables which hold the widgets data.
        """
        # self.should_clear_input = tk.IntVar(value=0)
        self.__browser = tk.StringVar(master, settings.CHROME)
        self.__browser.trace_add("write", self.__on_browser_changed)
        self.__path = tk.StringVar(master, '')
        self.__path.trace_add("write", self.__on_path_changed)
        self.__fetch_status = tk.StringVar(
            master, labels.DOWNLOAD_WEB_DRIVER)
        self.__selenium_type = tk.StringVar(
            master, settings.SELENIUM_TYPE_CLICK)
        self.__selenium_type.trace_add(
            "write", self.__on_selenium_type_changed)
        self.__selenium_by = tk.StringVar(
            master, settings.BY_ID)
        self.__instructions = tk.Variable(value=[])
        self.__by_value = tk.StringVar(master, '')
        self.__input_txt = tk.StringVar(master, '')
        self.__select_type = tk.StringVar(
            master, settings.SELECTION_HMTL_TEXT)
        self.__select_val = tk.StringVar(master, '')
        self.__curr_instruction = tk.StringVar(master, '')

    def __create_widgets(self):
        """
        Creates UI widgets.
        """

        label = tk.Label(self, text="Seleccioná el navegador")
        label.pack(anchor=tk.W)

        self.frame_0 = tk.Frame(
            self)  # , highlightbackground="black", highlightthickness=1)
        self.frame_0.pack(side=tk.TOP, fill=tk.X)

        self.radio_chrome = tk.Radiobutton(
            self.frame_0, text='Google Chrome',
            value='chrome', variable=self.__browser)
        self.radio_chrome.pack(anchor=tk.W)

        self.radio_edge = tk.Radiobutton(
            self.frame_0, text='Microsoft Edge',
            value='edge', variable=self.__browser)
        self.radio_edge.pack(anchor=tk.W)

        ttk.Separator(self, orient='horizontal').pack(
            fill='x', pady=settings.TTK_SEPARATOR_PADDING_Y)

        self.frame_1 = tk.Frame(
            self)  # , highlightbackground="black", highlightthickness=1)
        self.frame_1.pack(side=tk.TOP, fill=tk.X)

        self.label_select_driver = tk.Label(
            self.frame_1, text="Seleccioná el webdriver")
        self.label_select_driver.grid(
            row=0, column=0, sticky=tk.W)  # , pady = (10, 0))

        self.entry_file = tk.Entry(
            self.frame_1, width=60, textvariable=self.__path)
        self.entry_file.grid(row=1, column=0, sticky="ew")

        self.btn_entry_file = tk.Button(
            self.frame_1, text="...", height=1,
            padx=10, command=self.__select_file)
        self.btn_entry_file.grid(row=1, column=1, padx=10)

        self.frame_2 = tk.Frame(
            self)  # , highlightbackground="black", highlightthickness=1)
        self.frame_2.pack(side=tk.TOP, fill=tk.X)

        self.label_or = tk.Label(self.frame_2, text="ó")
        self.label_or.grid(row=0, column=0, sticky=tk.W)

        self.fetch_chrome_button = tk.Button(
            self.frame_2, text="Descargar Chrome", height=1, padx=10,
            width=15, command=self.__fetch_chrome)
        self.fetch_chrome_button.grid(row=1, column=0, sticky=tk.W)

        self.fetch_status_label = tk.Label(
            self.frame_2, textvariable=self.__fetch_status)
        self.fetch_status_label.grid(
            row=1, column=1, padx=5, sticky=tk.W)

        ttk.Separator(self, orient='horizontal').pack(
            fill='x', pady=settings.TTK_SEPARATOR_PADDING_Y)

        self.frame_3 = tk.Frame(self)
        self.frame_3.pack(side=tk.TOP, fill=tk.X)  # , pady=(10, 0))

        self.label_set_instructions = tk.Label(
            self.frame_3, text="Setear las instrucciones")
        self.label_set_instructions.grid(row=0, column=0, sticky=tk.W)

        self.frame_4 = tk.Frame(self)
        self.frame_4.pack(side=tk.TOP, fill=tk.X)

        self.label_action = tk.Label(self.frame_4, text="Acción", height=2)
        self.label_action.grid(row=1, column=0, sticky=tk.W)

        self.selenium_type_menu = tk.OptionMenu(
            self.frame_4, self.__selenium_type, *settings.SELENIUM_TYPE_LIST)
        self.selenium_type_menu.grid(row=1, column=1, sticky=tk.W)

        self.label_by = tk.Label(
            self.frame_4, text="Identificar por", height=2)
        self.label_by.grid(row=2, column=0, sticky=tk.W)

        self.selenium_by_menu = tk.OptionMenu(
            self.frame_4, self.__selenium_by, *settings.BY_LIST)
        self.selenium_by_menu.grid(row=2, column=1, sticky=tk.W)

        self.label_by_name = tk.Label(
            self.frame_4, text="Nombre identificador", height=2)
        self.label_by_name.grid(row=3, column=0, sticky=tk.W)

        self.selenium_by_val = tk.Entry(
            self.frame_4, width=35, textvariable=self.__by_value)
        self.selenium_by_val.grid(row=3, column=1, sticky="w")

        self.label_input_txt = tk.Label(
            self.frame_4, text="Texto a ingresar", height=2)
        self.label_input_txt.grid(row=4, column=0, sticky=tk.W)

        self.selenium_input_txt = tk.Entry(
            self.frame_4, width=35,
            textvariable=self.__input_txt)
        self.selenium_input_txt.config(state='disabled')
        self.selenium_input_txt.grid(row=4, column=1, sticky="w")

        self.label_selection_type = tk.Label(
            self.frame_4, text="Tipo selección", height=2)
        self.label_selection_type.grid(row=5, column=0, sticky=tk.W)

        self.selenium_selec_type = tk.OptionMenu(
            self.frame_4, self.__select_type,
            *settings.SELECTION_HTML_LIST)
        self.selenium_selec_type.config(state='disabled')
        self.selenium_selec_type.grid(row=5, column=1, sticky=tk.W)

        self.label_selection = tk.Label(
            self.frame_4, text="Selección", height=2)
        self.label_selection.grid(row=6, column=0, sticky=tk.W)

        self.seleniums_select_val = tk.Entry(
            self.frame_4, width=35,
            textvariable=self.__select_val)
        self.seleniums_select_val.config(state='disabled')
        self.seleniums_select_val.grid(row=6, column=1, sticky="w")

        self.frame_4_1 = tk.Frame(self.frame_4)
        self.frame_4_1.grid(row=7, column=0, columnspan=3, sticky=tk.W)

        self.btn_add_instructions = tk.Button(
            self.frame_4_1, text="Agregar", command=lambda: print("hello"))
        self.btn_add_instructions.grid(row=0, column=0, sticky=tk.W)

        self.label_current_action_title = tk.Label(
            self.frame_4_1, text="Estarías agregando:")
        self.label_current_action_title.grid(row=0, column=1, sticky=tk.W)

        self.label_current_action = tk.Label(
            self.frame_4_1, textvariable=self.__curr_instruction)
        self.label_current_action.grid(row=0, column=2, sticky=tk.W)

        ttk.Separator(self, orient='horizontal').pack(
            fill='x', pady=settings.TTK_SEPARATOR_PADDING_Y)

        self.frame_5 = tk.Frame(self)
        self.frame_5.pack(side=tk.TOP, fill=tk.X)

        self.label_instructions_list = tk.Label(
            self.frame_5, text="Instrucciones creadas")
        self.label_instructions_list.grid(
            row=0, column=0, sticky=tk.W, columnspan=3)

        spacer1 = tk.Label(self.frame_5, text="", width=100)
        spacer1.grid(row=1, column=0)

        self.listbox_instructions = tk.Listbox(
            self.frame_5, listvariable=self.__instructions,
            height=5, selectmode=tk.SINGLE)
        self.listbox_instructions.grid(
            row=1, column=0, sticky=tk.W+tk.E, rowspan=5)

        self.btn_del_instructions = tk.Button(
            self.frame_5, text="Eliminar", command=lambda: print("hello"))
        self.btn_del_instructions.grid(row=6, column=0, sticky=tk.W)

    def __select_file(self):
        """
        Runs an Open File Dialog for PDF selecting
        """
        try:
            downloads_path = str(Path.home())
            self.filename = filedialog.askopenfilename(
                initialdir=downloads_path,
                title="Seleccioná un webdriver .exe",
                filetypes=(("Archivos ejecutables", "*.exe"),)
            )
            if self.filename:
                self.entry_file.delete(0, 'end')
                self.entry_file.insert(0, self.filename)
                return
        except Exception as e:
            self.__popup(e)

    def __popup(self, message):
        """Displays error popup with the message provided
            parsed to string.
        Args:
            message (Any): gets parsed to a string.
        """
        error_title = "Ha ocurrido un error"
        error_message = "Error: " + str(message)
        messagebox.showerror(error_title, error_message)
        return

    def __on_browser_changed(self, *args, **kwargs):
        if self.__browser.get() == "chrome":
            self.fetch_chrome_button["state"] = "normal"
        else:
            self.fetch_chrome_button["state"] = "disabled"
        return True

    def __on_path_changed(self, *args, **kwargs):
        path = self.__path.get()
        settings.save_setting(settings.DRIVER_PATH_KEY, path)
        return True

    def __on_selenium_type_changed(self, *args, **kwargs):
        val = self.__selenium_type.get()
        opts = [(self.selenium_input_txt, settings.SELENIUM_TYPE_FILL),
                (self.selenium_selec_type, settings.SELENIUM_TYPE_SELECT),
                (self.seleniums_select_val, settings.SELENIUM_TYPE_SELECT)]
        for w, v in opts:
            if val == v:
                w.config(state='normal')
            else:
                w.config(state='disabled')
        # if val == settings.SELENIUM_TYPE_CLICK:
        #     self.selenium_input_txt.config(state='disabled')
        #     self.selenium_selec_type.config(state='disabled')
        #     self.seleniums_select_val.config(state='disabled')
        # elif val == settings.SELENIUM_TYPE_FILL:
        #     self.selenium_input_txt.config(state='normal')
        #     pass
        # elif val == settings.SELENIUM_TYPE_SELECT:
        #     self.selenium_selec_type.config(state='normal')
        #     self.seleniums_select_val.config(state='normal')
        # else:
        #     raise ValueError(f"Selenium type can not be {val}")

    def __fetch_chrome(self):
        """
        Download Google Chrome's web-driver for current version.
        """
        def on_done():
            self.__path.set(os.path.join(os.getcwd(), "chromedriver.exe"))
            self.fetch_chrome_button["state"] = "normal"
            self.__fetch_status.set("Listo!")
        self.fetch_chrome_button["state"] = "disabled"
        self.__fetch_status.set("Descargando...")
        async_fetch_chrome = AsyncFetchChrome(on_done)
        async_fetch_chrome.start()

    def __string_var_or_none(self, string_var):
        if ret := string_var.get() != '':
            return ret
        return None

    def __get_current_instruction(self):
        try:
            _type = self.__string_var_or_none(self.__select_type)
            _by = self.__string_var_or_none(self.__selenium_by)
            _by_val = self.__string_var_or_none(self.__by_value)
            _input_txt = self.__string_var_or_none(self.__input_txt)
            _select_type = self.__string_var_or_none(self.__select_type)
            _select_val = self.__string_var_or_none(self.__select_val)
            build_instruction(_type, _by, _by_val, _input_txt,
                              _select_type, _select_val)
        except ValueError:
            return labels.INSUFFICIENT_DATA


class AsyncFetchChrome(Thread):
    def __init__(self, callback: Callable, *callable_args, **callable_kwargs):
        super().__init__()
        self.callback = callback
        self.callable_args = callable_args
        self.callable_kwargs = callable_kwargs

    def run(self):
        get_driver = GetChromeDriver()
        get_driver.download_stable_version(
            output_path=os.getcwd(), extract=True)
        self.callback(*self.callable_args, **self.callable_kwargs)


"""
click button
click checkbox
fill field
select option
"""
