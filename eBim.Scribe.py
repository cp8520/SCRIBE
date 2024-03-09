import sys
import flet as ft
import pyperclip
from zoneinfo import ZoneInfo
from datetime import datetime
import winreg
# import subprocess
class DarkMode:
    # def is_dark_mode_mac():
    #     command = '''
    #         tell application "System Events"
    #             tell appearance preferences
    #                 set dark_mode to dark mode
    #             end tell
    #         end tell
    #         return dark_mode
    #     '''
    #     result = subprocess.run(['osascript', '-e', command], capture_output=True, text=True)
    #     return result.stdout.strip() == "true"

    # if is_dark_mode_mac():
    #     print("Darkmode on")
    #     pass
    # else:
    #     print("Darkmode off")
    #     pass

    def is_dark_mode_windows():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception as e:
            print(f"Error: {e}")
            return False

    if is_dark_mode_windows():
        print("Darkmode on")
        pass
    else:
        print("Darkmode off")
        pass

class Data:
    def __init__(self) -> None:
        self.counter = 0

d = Data()

def main(page: ft.Page):
    DarkMode.is_dark_mode_windows()
    # DarkMode.is_dark_mode_mac()
    page.window_min_height = 680
    page.window_min_width = 320
    page.auto_scroll = True

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )  

    def count_up(e):
        d.counter += 1
        page.update()
    
    def count_down(e):
        d.counter -= 1
        page.update()

    def open_snackbar(e):
        page.snack_bar = ft.SnackBar(ft.Row([
            # ft.IconButton(ft.icons.ADD,on_click=count_up),
            # ft.IconButton(ft.icons.REMOVE,on_click=count_down),
            # ft.IconButton(ft.icons.SELECT_ALL,on_click=lambda e: manipulate_input_field_copy(e,tabs_control.selected_index)),
            ft.IconButton(ft.icons.COPY_ALL,on_click=lambda e: manipulate_input_field_copy(e,tabs_control.selected_index),on_focus=ft.icons.COPY_ALL_OUTLINED),
            # ft.IconButton(ft.icons.CUT),
            ft.IconButton(ft.icons.PASTE,on_click=lambda e: manipulate_input_field_paste(e,tabs_control.selected_index),on_focus=ft.icons.PASTE_OUTLINED),
            
        ]))
        page.snack_bar.open = True
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)
    
    def insert_timestamp(event):
        pacifictime = datetime.now(ZoneInfo('America/Los_Angeles')).replace(tzinfo=None).isoformat(sep=" ",timespec="seconds")
        event.control.value += f"\n{pacifictime} >>> "
        page.update()
    
    def create_input_field():
        input_field = ft.TextField(
            min_lines=20,max_lines=20, autocorrect=True, hint_text="Start scribing!",
            enable_suggestions=True, multiline=True,shift_enter=True, on_submit=insert_timestamp,show_cursor=True,on_focus=insert_timestamp
            )
        input_fields.append(input_field)
        return input_field
    def check_tab_index(event,index):
        print(f"CLICKED & Index={index}")

    tabs_list = []
    tabs_index = []
    input_fields = []

    def manipulate_input_field_copy(event,index):
        selected_index = index
        if 0 <= selected_index < len(input_fields):
            current_input_field = tabs_control.selected_index
            for current_input_field in input_fields:
                pyperclip.copy(current_input_field.value)
                create_input_field.value = "Copied"
                page.update()

    def manipulate_input_field_paste(event,index):
        selected_index = index
        if 0 <= selected_index < len(input_fields):
            tabs_control.selected_index = tabs_control.selected_index
            for current_input_field in input_fields:
                input_fields[tabs_control.selected_index].value = None
                input_fields[tabs_control.selected_index].value = pyperclip.paste()
                page.update()

            

    def add_tab(event):
        t = build_tab()
        tabs_list.append(t)  
        tabs_control.tabs = tabs_list  
        tabs_control.selected_index = len(tabs_list) - 1
        page.update()
    
    def close_tab(e,index):
        tabs_control.tabs = tabs_list  
        try:
            tabs_list.pop(index)
            tabs_control.selected_index = len(tabs_list)-1
        except:
            tabs_list.pop()
        page.update()

    def close_tabs(e):  
        tabs_list.clear()
        page.update()

    def close_app(event):
        print("exit")
        quit()

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        add_tab(e)
        e.control.checked = not e.control.checked
        page.update()

    tabs_control = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=tabs_list,
        expand=0,    
        ) 

    def build_tab():
        new_tab = ft.Tab(text=f"eBim {len(tabs_list)+1}",  content=ft.Column([            
            create_input_field(),
            ft.Row([            
                # ft.Text(f"Count: {d.counter}"),
                ft.Text(f"Tools: "),
                ft.IconButton(ft.icons.ABC,on_click=lambda e: open_snackbar(e))]),

            ]))
        return new_tab

    page.appbar = ft.AppBar(
    leading=ft.PopupMenuButton(tooltip="Menu",icon=ft.icons.MENU,items=[
                ft.PopupMenuItem(text="Add Tab",checked=False,on_click=lambda e: add_tab(e)),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Remove Tab",checked=False,on_click=lambda e: close_tab(e,tabs_control.selected_index)),                
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Close All Tabs",checked=False,on_click=lambda e: close_tabs(e)),
                ]),
    leading_width=50,
    title=ft.Text("eBim SCRIBE"),
    center_title=True,
    bgcolor=ft.colors.SURFACE_VARIANT,
    actions=[
        # ft.PopupMenuButton(icon=ft.icons.SAVE_ALT,tooltip="Save Notes",
        #     items=[
        #         ft.PopupMenuItem(),
        #         ft.PopupMenuItem(text="Save Tabs",checked=False,on_click=lambda _: pick_files_dialog.pick_files(
        #             allow_multiple=True
        #         ))
        #     ]
        # ),
    ],
)

    add_tab_button = ft.IconButton(icon="PLAYLIST_ADD", on_click=lambda e: add_tab(e, build_tab))
    add_close_app_button = ft.IconButton(icon="CLOSE", on_click=close_app,)
    add_close_tab_button = ft.IconButton(icon="PLAYLIST_REMOVE", on_click=lambda e: close_tab(e,tabs_control.selected_index))

    page.add(tabs_control)


ft.app(target=main)
