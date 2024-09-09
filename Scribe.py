import sys
import flet as ft
from zoneinfo import ZoneInfo
from datetime import datetime
import requests
import pickle
import time

class ApiService:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        auth_url = f"{self.base_url}/auth/token"  # Replace with your actual auth endpoint
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(auth_url, json=payload)
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                print(f"Authentication successful! Token: {self.token}")
            else:
                print(f"Failed to authenticate: {response.status_code} {response.text}")
        except Exception as ex:
            print(f"An error occurred during authentication: {ex}")

    def get_headers(self):
        """Returns headers with the authentication token."""
        if self.token:
            return {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
        else:
            return {
                'Content-Type': 'application/json'
            }

    def make_authorized_request(self, endpoint):
        """Example of making a request with an authenticated token."""
        headers = self.get_headers()
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to retrieve data: {response.status_code} {response.text}")
                return None
        except Exception as ex:
            print(f"An error occurred during the request: {ex}")
            return None

class Observer:
    def update(self, message):
        try:
            raise NotImplementedError("Subclass must implement abstract method")
        except Exception as ex:
            print(f"ERROR: {ex}")

class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self,function):
        for observer in self._observers:
            observer.update()

class PageObserver(Observer):
    def __init__(self, page: ft.Page):
        self.page = page
        self.tabs = ScribeTabs

    def update(self):
        self.page.update()

    def close_app(self):
        self.page.window_close()

class TimestampGenerator(Observer):
    def __init__(self, page: ft.Page):
        self.page = page

    def generate_timestamp(self, event):
        pacifictime = datetime.now(ZoneInfo('America/Los_Angeles')).replace(tzinfo=None).isoformat(sep=" ", timespec="seconds")
        event.control.value += f"\n{pacifictime} >>> "
        event.page.update()

    def plain_time():
        time = datetime.now(ZoneInfo('America/Los_Angeles')).replace(tzinfo=None).isoformat(timespec="hours")
        t = datetime.now(ZoneInfo('America/Los_Angeles')).now().date()
        return time

    def update(self):
        self.page.update()

class ErrorHandler:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def update(self):
        self.page.update()
    
    def throw(message):        
        error = ft.Text(message,text_align=ft.MainAxisAlignment.CENTER,scale=.75)
        i = ft.Icon(ft.icons.WARNING)
        row = ft.Row(controls=[i,error],spacing=30,alignment=ft.MainAxisAlignment.SPACE_EVENLY,vertical_alignment=ft.MainAxisAlignment.CENTER,wrap=True)
        dlg = ft.AlertDialog(title=row,content_padding=20,actions=[],modal=False,)
        return dlg
    
    def safety_net(message):
        error = ft.Text(message,text_align=ft.MainAxisAlignment.CENTER,scale=.75)
        i = ft.Icon(ft.icons.WARNING)
        xmark = ft.IconButton(icon=ft.icons.CLOSE,on_click=lambda self: self.page.close(dlg_modal))
        row = ft.Row(controls=[i,error],spacing=30,alignment=ft.MainAxisAlignment.SPACE_EVENLY,vertical_alignment=ft.MainAxisAlignment.CENTER,wrap=True)
        dlg_modal = ft.AlertDialog(title=row,content_padding=20,actions=[xmark],modal=True,on_dismiss=lambda self: self.page.close(dlg_modal),actions_alignment=ft.MainAxisAlignment.CENTER)
        return dlg_modal
    
class DataHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        self.time_gen = TimestampGenerator
    
    def update(self):
        self.page.update()
    
    def save_text(self,text):
        t = text
        timestamp = int(time.time()) 
        i = []
        filename = f"tab_{timestamp}_"
        i.append(t)
        with open(f"{filename}.pkl","wb") as f:
            pickle.dump(i, f)

    def save_preferences(self,text):
        t = text
        i = []
        filename = "user_prefs.pkl"
        i.append(t)
        with open(f"{filename}.pkl","wb") as f:
            pickle.dump(i, f)

    def update_index(filename):
        index_filename = "index.pkl"
        try:
            with open(index_filename, "rb") as f:
                index = pickle.load(f)
        except FileNotFoundError:
            index = []
        index.append(filename)

        with open(index_filename, "wb") as f:
            pickle.dump(index, f)

    def load_text(self,index):
        loaded_i = index
        i=[]
        i = loaded_i
        with open(f"text.pkl","rb") as f:
            i = pickle.load(f)
            return i
        


class ColorSelector:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_color_index = 0

    def update(self):
        self.page.update()

    def cycle_tab_colors(self, e, color_storage):
        self.current_color_index = (self.current_color_index + 1) % len(self.color_list)
        new_color = self.color_list[self.current_color_index]
        color_storage = new_color
        ScribeTabs.set_tab_color(self,new_color)
        self.update()

    def cycle_text_colors(self,e,color_storage):
        self.current_color_index = (self.current_color_index+1)%len(self.color_list)
        new_color = self.color_list[self.current_color_index]
        color_storage = new_color
        ScribeTabs.set_text_color(self,new_color)
        self.update()


class ScribeTabs(Observer):
    def __init__(self, page: ft.Page):
        self.page = page
        # self.api_service = ApiService("https://api.example.com")
        self.time = TimestampGenerator
        self.tabs_list = []
        self.input_fields_list = []
        self.close_buttons_list = []
        self.tabs_control = ft.Tabs(
            selected_index=0,
            tabs=self.tabs_list,
            indicator_color=ft.colors.BLUE,
            label_color=ft.colors.BLUE,
            overlay_color=ft.colors.BLUE_900,
            divider_color=ft.colors.BLUE_900,
            indicator_padding=5,
            scrollable = True,
            animation_duration=800,
            right=True
        )
        self.color_list = ["RED","YELLOW","GREEN", "BLUE","INDIGO","SURFACE_VARIANT"]
        self.current_color_index = 0
        self.err = ErrorHandler.throw
        self.confirm_close = ErrorHandler.safety_net
        self.save = DataHandler.save_text
        self.load = DataHandler.load_text

    def update(self):
        self.page.update()

    def set_tab_color(self,color):
        self.tabs_control.indicator_color = color
        self.tabs_control.label_color = color
        self.tabs_control.overlay_color = f"{color}900"
        self.tabs_control.divider_color = f"{color}900"
        self.update()    
        
    def set_text_color(self,color):
        index = self.input_fields_list.index(self)
        self.input_fields_list[index].text_color = ft.colors.AMBER
        self.update()

    def fetch_data(self, e):
        # Example API call
        data = self.api_service.get_data("some-endpoint")
        if data:
            self.display_data(data)
        else:
            print("Failed to fetch data")

    def display_data(self, data):
        self.page.add(ft.Text(f"API Data: {data}"))
        self.page.update()

    def generate_tab_container(self):
        tab_container = ft.Container(content=ft.Column([self.tabs_control],expand=1))
        return tab_container

    def get_input_indexes_with_value(self):
        index = self.input_fields_list
        for i in index:
            try:
                print("Something?")
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION: {ex}"))
            else:
                self.page.open("Nothing happened.")
    
    def close_scribe_tab(self, e, tab):
        tab_index = self.tabs_list.index(tab)
        input_index = self.input_fields_list[tab_index]
        time = self.time.plain_time()
        t = ft.Text(value=time).value
        if len(input_index.value)<=0:
            try:
                self.tabs_list.remove(tab)
                self.input_fields_list.remove(input_index)
                self.tabs_control.tabs = self.tabs_list
                self.page.update()
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION @ remove empty tab: {ex}"))
        elif len(input_index.value)>=1:
            try:
                self.save(self,input_index.value)
                self.tabs_list.remove(tab)
                self.input_fields_list.remove(input_index)
                self.tabs_control.tabs = self.tabs_list
                self.page.update()
                self.page.open(self.confirm_close(f"Tab data was saved to history!"))
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION @ remove saved tab: {ex}"))

    def close_tab(self,e,tab):
        self.tabs_list.remove(tab)
        self.tabs_control.tabs = self.tabs_list
        self.page.update()
            

    def add_tab(self, e):
        tc = self.tabs_control
        if len(tc.tabs) < 50:
            try:
                new_index_position = len(self.tabs_list)
                t = self.generate_tab(new_index_position)
                tc.tabs.append(t)
                self.tabs_list = tc.tabs
                self.page.update()
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION: {ex}"))
        else:
            self.page.open(self.err("Max amount of tabs reached!"))

    def add_tab_with_content(self, content):
        tc = self.tabs_control
        if len(tc.tabs) < 50:
            try:
                new_index_position = len(self.tabs_list)
                t = self.generate_tab(new_index_position, content)
                tc.tabs.append(t)
                self.tabs_list = tc.tabs
                self.page.update()
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION: {ex}"))
        else:
            self.page.open(self.err("Max amount of tabs reached!"))

    def generate_tab(self, index, content=None):
        # Generate timestamp
        t = TimestampGenerator(self.page).generate_timestamp
        
        name_tab_field = ft.TextField(
            hint_text=f"Scribe Tab",
            width=100, border_width=0, content_padding=1
        )
        
        input_field = ft.TextField(
            autofocus=True, hint_text="Start Scribing!",
            shift_enter=True, multiline=True, expand=True,
            icon=ft.icons.INPUT, on_submit=t,
            content_padding=20, show_cursor=True,
            max_lines=20, dense=True, border_width=0, adaptive=True,
            value=content if content else "",  # Use content if provided
        )

        self.input_fields_list.append(input_field)
        
        close_button = ft.IconButton(
            icon=ft.icons.CLOSE, on_click=lambda e: self.close_scribe_tab(e, tab),
            focus_color="RED", highlight_color="RED",
            selected_icon_color="RED", scale=.5, hover_color="RED"
        )

        tab_icon = ft.Icon(ft.icons.TAB, scale=.75)
        
        tab_content = ft.Container(content=input_field, padding=20)
        tab = ft.Tab(
            tab_content=ft.Row(controls=[tab_icon, name_tab_field, close_button]),
            content=ft.Container(
                ft.ResponsiveRow([ft.Column([tab_content])], rtl=False, alignment=ft.MainAxisAlignment.SPACE_EVENLY, expand=True, run_spacing=1)
            )
        )
        return tab
    
    def add_prefs_tab(self, e):
        tc = self.tabs_control
        if len(tc.tabs) < 5:
            try:
                new_index_position = len(self.tabs_list)
                t = self.generate_prefs_tab(new_index_position)
                tc.tabs.append(t)
                self.tabs_list = tc.tabs
                self.page.update()
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION: {ex}"))
        else:
            self.page.open(self.err("Max amount of tabs reached!"))



    def generate_prefs_tab(self, index):
        close_button = ft.IconButton(
            icon=ft.icons.CLOSE,on_click=lambda e: self.close_tab(e, tab),focus_color="RED",highlight_color="RED",
            selected_icon_color="RED",scale=.5,hover_color="RED"
        )
        cs = ColorSelector
        name_tab_field = ft.Text(
            value=f"Preferences",
        )
        tab_icon = ft.Icon(ft.icons.EDIT,scale=.75)
        tab_color_select_button = ft.TextButton(
                        "Tab Indicator Color",
                        icon=ft.icons.COLOR_LENS,
                        icon_color=self.tabs_control.overlay_color,
                        on_click=lambda e: cs.cycle_tab_colors(self,e, self.tabs_control.indicator_color),
                        
                    )
        text_color_select_button = ft.TextButton(
                        "Text Color",
                        icon=ft.icons.FORMAT_COLOR_TEXT,
                        icon_color=self.tabs_control.overlay_color,
                        on_click=lambda e: cs.cycle_text_colors(self,e, self.tabs_control.indicator_color),
                        
                    )
        if self.page.window_full_screen is False:
            tab_content = ft.Container(
                content=ft.Container(
                    content=ft.Column([tab_color_select_button,text_color_select_button]),padding=20
                )
            )
            self.page.update()
        tab = ft.Tab(
            tab_content=ft.Row([tab_icon,name_tab_field,close_button]),
            content=ft.Container(
                ft.Column([
                    ft.Column([
                        tab_content
                        ])],
                        auto_scroll=True,scroll=True,expand=True)),
        )
        return tab

    def add_config_tab(self, e):
        tc = self.tabs_control
        if len(tc.tabs) < 5:
            try:
                new_index_position = len(self.tabs_list)
                t = self.generate_config_tab(new_index_position)
                tc.tabs.append(t)
                self.tabs_list = tc.tabs
                self.page.update()
            except Exception as ex:
                self.page.open(self.err(f"EXCEPTION: {ex}"))
        else:
            self.page.open(self.err("Max amount of tabs reached!"))

    def generate_config_tab(self, index):
        close_button = ft.IconButton(
            icon=ft.icons.CLOSE,on_click=lambda e: self.close_tab(e, tab),focus_color="RED",highlight_color="RED",
            selected_icon_color="RED",scale=.5,hover_color="RED"
        )
        name_tab_field = ft.Text(
            value=f"Configuration",
        )
        tab_icon = ft.Icon(ft.icons.SETTINGS,scale=.75)
        if self.page.window_full_screen is False:
                tab_content = ft.Container(content=ft.Container(content=ft.Radio("Auto Scroll",value=True,toggleable=True),padding=20))
        else:
                tab_content = ft.Container(content=ft.Container(content=ft.Radio("Auto Scroll",value=False,toggleable=True),padding=20))
        tab = ft.Tab(
            tab_content=ft.Row([tab_icon,name_tab_field,close_button]),
            content=ft.Container(ft.Column([ft.Column([tab_content])],auto_scroll=True,scroll=True,expand=True))
        )
        return tab
    
    def add_loaded_tab(self,e):
        index = self.load
        self.generate_tab(index)

class FileSelector(Observer):
    def __init__(self, page: ft.Page, data_handler: DataHandler, scribe_tabs: ScribeTabs):
        self.page = page
        self.data_handler = data_handler
        self.scribe_tabs = scribe_tabs
        self.selected_files = ft.Text()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)

    def update(self):
        self.page.update()

    def clean_data(self, content):
        if isinstance(content, str):
            cleaned_content = " ".join(content.splitlines()).strip()
        elif isinstance(content, list):
            cleaned_content = " ".join([line.strip() for line in content if line.strip()])
        else:
            cleaned_content = str(content)
        
        return cleaned_content

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_files.value = ", ".join([f.name for f in e.files])
            for file in e.files:
                with open(file.path, "rb") as f:
                    content = pickle.load(f)
                    cleaned_content = self.clean_data(content)
                    self.scribe_tabs.add_tab_with_content(cleaned_content)
        else:
            self.selected_files.value = "Cancelled!"
        self.selected_files.update()

def main(page: ft.Page):
    page.window_resizable = True
    page.window_frameless = True
    page.window_full_screen = False
    page.window_min_height = 320
    page.window_min_height = 640 
    page.window_opacity = 20
    page.auto_scroll = True
    page.window_center()
    page.window_frameless = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True

    subject = Subject()
    data_handler = DataHandler(page)
    observer1 = ScribeTabs(page)
    observer2 = PageObserver(page)
    observer3 = FileSelector(page, data_handler, observer1)

    subject.add_observer(observer1)
    subject.add_observer(observer2)
    subject.add_observer(observer3)


    def on_fetch_data_button_click(e):
        subject.notify_observers(observer1.fetch_data(e))

    def on_add_tab_button_click(e):
        subject.notify_observers(observer1.add_tab(e))

    def on_close_window_button_click(e):
        subject.notify_observers(observer2.close_app())

    def on_edit_preferences_button_click(e):
        subject.notify_observers(observer1.add_prefs_tab(e))

    def on_edit_configuration_button_click(e):
        subject.notify_observers(observer1.add_config_tab(e))

    add_tab_button = ft.FloatingActionButton(
        icon=ft.icons.NOTE_ADD,
        bgcolor=ft.colors.SURFACE_VARIANT,
        on_click=on_add_tab_button_click,
        foreground_color="GREEN_600",
        focus_color="GREEN")
    
    tab_container = ft.Container(
        observer1.generate_tab_container()
        )
    
    app_bar = ft.AppBar(
        leading=ft.Icon(
            ft.icons.NOTE_ALT
            ),
        leading_width=40,
        title=ft.WindowDragArea(
            ft.Container(
                ft.Text("SCRIBE"),
                padding=20,scale=1.5
                )),title_text_style=ft.TextStyle(italic=True),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Configuration",icon=ft.icons.SETTINGS,on_click=on_edit_configuration_button_click),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Preferences",icon=ft.icons.EDIT,on_click=on_edit_preferences_button_click),                    
                    ft.PopupMenuItem(),  # divider                    
                    ft.PopupMenuItem(text="Load", icon=ft.icons.FILE_OPEN, on_click=lambda _: observer3.pick_files_dialog.pick_files(allow_multiple=False)),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Close Application",icon=ft.icons.CLOSE_ROUNDED,on_click=on_close_window_button_click),
                ]
            ),
        ],)

    page.add(app_bar, add_tab_button, tab_container)

ft.app(target=main)