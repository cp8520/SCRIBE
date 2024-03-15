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
    page.auto_scroll = False
    page.window_opacity = 5
    page.window_frameless = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_center()
    

    tabs_list = []
    tabs_index = []
    input_fields = []
    tab_names = ["Scribe Tab"]
    
    def set_tab_name(name, index):
        # Ensure index is an integer
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")

        if name is None:
            name = "New Tab"
        elif 0 <= index < len(tab_names):
            tab_names.insert(index, name)
        else:
            # Handle the case where index is out of bounds, if needed
            print("Index is out of the valid range.")
        page.update()

    def get_window_size():
        h = page.height
        w = page.width
        page.update()
        return w,h

    def open_adaptive_dialog(e):
        page.dialog = adaptive_alert_dialog
        adaptive_alert_dialog.open = True
        page.update()

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
            ft.IconButton(ft.icons.CONTENT_COPY,on_click=lambda e: manipulate_input_field_copy(e,tabs_control.selected_index),on_focus=ft.icons.COPY_ALL_OUTLINED),
            # ft.IconButton(ft.icons.CUT),
            ft.IconButton(ft.icons.PASTE,on_click=lambda e: manipulate_input_field_paste(e,tabs_control.selected_index),on_focus=ft.icons.PASTE_OUTLINED),
            
        ]))
        page.snack_bar.open = True
        page.snack_bar.bgcolor = ft.colors.GREY_800
        page.snack_bar.opacity = 90
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
        W,H = get_window_size()
        heightData = H
        if heightData != H:
            page.update
        input_field = ft.TextField(
            min_lines=20,max_lines=20, autocorrect=True, hint_text="Click to Start Scribing!",height=H,
            enable_suggestions=True, multiline=True,shift_enter=True, on_submit=insert_timestamp,show_cursor=True
            )
        input_fields.append(input_field)
        return input_field
    
    def check_tab_index(event,index):
        print(f"CLICKED & Index={index}")

    def manipulate_input_field_copy(event, index):
        if 0 <= index < len(input_fields):
            field_to_copy = input_fields[index]
            if field_to_copy:
                pyperclip.copy(field_to_copy.value)
                create_input_field.value = "Copied"
                page.update()
            else:
                print(f"Error: No input field exists at index {index}.")

    def manipulate_input_field_paste(event, index):
        if 0 <= index < len(input_fields):
            target_field = input_fields[index]
            if target_field:
                target_field.value = pyperclip.paste()
                page.update()
            else:
                print(f"Error: No input field exists at index {index}.")

    def add_tab(event):
        t = build_tab()
        tabs_list.append(t)  
        tabs_control.tabs = tabs_list  
        tabs_control.selected_index = len(tabs_list) - 1
        page.update()
    
    def close_tab(e, index):
        if 0 <= index < len(tabs_list):
            try:
                tabs_list.pop(index)
                input_fields.pop(index)
                tabs_control.tabs = tabs_list
                tabs_control.selected_index = min(index, len(tabs_list) - 1)
            except Exception as ex:
                print(f"An error occurred: {ex}")
        else:
            print("Error: Invalid index for tab closure.")
        page.update()

    def close_tabs(e):  
        tabs_list.clear()
        tabs_list.sort()
        tabs_control.selected_index = 0
        page.update()

    def close_app(event):
        print("exit")
        page.window_close()

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
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=add_tab, bgcolor=ft.colors.GREY_800
    )
    def name_current_tab(e,index):
        input = ft.TextField(on_submit=lambda index: set_tab_name(input, index))
        page.update()
        if 0 <= index < len(tabs_list)-1:
            tab_names[index] = input.value

    def build_tab():
        new_tab = ft.Tab(tab_content=ft.Row([
            ft.TextButton(
            f"{tab_names[0]}",
            on_click=lambda e: name_current_tab(e,tabs_control.selected_index),
            disabled=True)]),
            content=ft.Column([    
            create_input_field(),
            ]))
        set_tab_name("Scribe Tab",tabs_control.selected_index)
        return new_tab

    page.appbar = ft.AppBar(
    leading=ft.PopupMenuButton(tooltip="Menu",icon=ft.icons.MENU,items=[
                # ft.PopupMenuItem(text="Add Tab",checked=False,on_click=lambda e: add_tab(e)),
                # ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Remove Tab",checked=False,on_click=lambda e: close_tab(e,tabs_control.selected_index)),                
                ft.PopupMenuItem(),
                # ft.PopupMenuItem(text="Close All Tabs",checked=False,on_click=lambda e: close_tabs(e)),
                ]),
    leading_width=50,
    title=ft.WindowDragArea(ft.Container(ft.Text("SCRIBE"),padding=20)),
    center_title=True,
    bgcolor=ft.colors.SURFACE_VARIANT,
    actions=[ft.Row([
        ft.Divider(),
        ft.IconButton(ft.icons.ABC_ROUNDED, on_click= lambda e: open_snackbar(e)),
        ft.Divider(),
        ft.IconButton(ft.icons.CLOSE,on_click=close_app),
        ft.Divider(),
        ft.Text("V1.1.26",tooltip="by Christian Paustell"),
        
        ft.Divider(),
    ])
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

    actions = []
    if page.platform in ["ios", "macos"]:
        actions = [
            ft.CupertinoDialogAction("OK"),
            ft.CupertinoDialogAction("Cancel"),
        ]
    else:
        actions = [ft.TextButton("OK",on_click=lambda e:name_current_tab(e,tabs_control.selected_index))]
                
    drag_area = ft.WindowDragArea(ft.Container(ft.Text("Drag this area to move, maximize and restore application window."), padding=10), expand=True),


    adaptive_alert_dialog = ft.AlertDialog(
        adaptive=True,
        title=ft.Text("Name this tab?"),
        content=ft.TextField(show_cursor=True,multiline=False,max_lines=1,animate_size=2),
        actions=actions,
    )
    add_tab_button = ft.IconButton(icon="PLAYLIST_ADD", on_click=lambda e: add_tab(e, build_tab))
    add_close_app_button = ft.IconButton(icon="CLOSE", on_click=close_app,)
    add_close_tab_button = ft.IconButton(icon="PLAYLIST_REMOVE", on_click=lambda e: close_tab(e,tabs_control.selected_index))

    page.add(ft.Container(tabs_control, padding=10)
)


ft.app(target=main)
