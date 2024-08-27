import sys
import flet as ft
import pyperclip
from zoneinfo import ZoneInfo
from datetime import datetime
class app_settings:
     selected_indicator_color = int

def main(page: ft.Page):
    page.window_center()
    page.window_min_height = 680
    page.window_min_width = 320
    page.window_opacity = 23
    page.window_frameless = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True
    
    indicator_colors = ["RED","YELLOW","BLUE"]

    tabs_list = []

    input_fields = []

    last_error_code = int

    tab_names = [
         "NoteTab"
         ]
    
    welcome_message = ["Welcome to Scribe!\n\nBy Christian Paustell\nVersion 1.1.27"]

    error_messages = [
         "Too many tabs, close tabs first...", 
         "No text field to copy..."
         ]
    
    tabs_control = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=tabs_list,
        indicator_border_radius=10,
        indicator_color="RED",
        indicator_padding=4, 
        indicator_tab_size=16,
        )

    col = ft.Column(horizontal_alignment=ft.MainAxisAlignment.END,spacing=3)

    def handle_errors(number):
         index = number
         return index
         

    def get_window_size():
        page.update()
        h = page.height
        w = page.width
        return w,h
    
    def choose_indicator_color(e,index):
         app_settings.selected_indicator_color = indicator_colors[index]
         tabs_control.indicator_color = "".join(indicator_colors[int(i)] for i in str(app_settings.selected_indicator_color))
    
    def create_input_field():
            W,H = get_window_size()
            heightData = H
            if page.window_maximized == True:
                input_field = ft.TextField(
                    max_lines=50,
                    autocorrect=True, hint_text="Press Enter to Start Scribing!",height=H,
                    enable_suggestions=True, multiline=True,shift_enter=True, on_submit=insert_timestamp,show_cursor=True,border_width=0,adaptive=True,content_padding=0,
                    )
                input_field.content_padding = 10
                input_fields.append(input_field)            
                page.update()
                return input_field
            else:
                
                input_field = ft.TextField(
                    max_lines=20,
                    autocorrect=True, hint_text="Press Enter to Start Scribing!",height=H,
                    enable_suggestions=True, multiline=True,shift_enter=True, on_submit=insert_timestamp,show_cursor=True,border_width=0,adaptive=True,content_padding=0,
                    )
                input_field.content_padding = 10
                input_fields.append(input_field)
                page.update()
                return input_field
            
    def insert_timestamp(event):
            pacifictime = datetime.now(ZoneInfo('America/Los_Angeles')).replace(tzinfo=None).isoformat(sep=" ",timespec="seconds")
            event.control.value += f"\n{pacifictime} >>> "
            page.update()
            
    def input_field_copy(event, index):
        if 0 <= index < len(input_fields):
            field_to_copy = input_fields[index]
            if field_to_copy:
                pyperclip.copy(field_to_copy.value)
                create_input_field.value = "Copied"
                page.update()
            else:
                open_adaptive_dialog()
                print(f"Error: No input field exists at index {index}.")

    def input_field_paste(event, index):
        index = tabs_control.selected_index
        if 0 <= index < len(input_fields):
            target_field = input_fields[index]
            if target_field:
                target_field.value = pyperclip.paste()
                page.update()
            else:
                print(f"Error: No input field exists at index {index}.")

    def open_adaptive_dialog(e):
        page.dialog = adaptive_alert_dialog
        adaptive_alert_dialog.open = True
        page.update()

    def open_snackbar(e):
            page.snack_bar = ft.SnackBar(ft.Row([
                # ft.IconButton(ft.icons.ADD,on_click=count_up),
                # ft.IconButton(ft.icons.REMOVE,on_click=count_down),
                # ft.IconButton(ft.icons.SELECT_ALL,on_click=lambda e: manipulate_input_field_copy(e,tabs_control.selected_index)),
                ft.IconButton(ft.icons.CONTENT_COPY,on_click=lambda e: input_field_copy(e,tabs_control.selected_index),on_focus=ft.icons.COPY_ALL_OUTLINED),
                # ft.IconButton(ft.icons.CUT),
                ft.IconButton(ft.icons.PASTE,on_click=lambda e: input_field_paste(e,tabs_control.selected_index),on_focus=ft.icons.PASTE_OUTLINED),
                
            ]))
            page.snack_bar.open = True
            page.snack_bar.bgcolor = ft.colors.GREY_800
            page.snack_bar.opacity = 90
            page.update()

    def number_to_words(number):
        words = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
        return " ".join(words[int(i)] for i in str(number))
    
    adaptive_alert_dialog = ft.AlertDialog(
        adaptive=True,
        content=ft.Text(f"{error_messages[last_error_code]}\n\n Click away from this box to continue.",text_align="CENTER"),
        icon=ft.Icon(ft.icons.WARNING),
        title=ft.Text(f"WARNING!",text_align="CENTER"),
        )
    
    def build_tab():
            new_tab = ft.Tab(tab_content=ft.Row([
            ft.TextField(dense=True,filled=True,focused_border_width=1,border=False,text_align="LEFT",prefix_icon=ft.icons.TAB,text_size=18,max_lines=1,scale=.8,
            hint_text=(f"{tab_names[tabs_control.selected_index]} {number_to_words(len(tabs_list))}"),
            on_submit=lambda e: name_current_tab(e,tabs_control.selected_index),width=200,border_width=0,border_radius=5,
            disabled=False,)
            ]),
            content=ft.Column([col,ft.IconButton(icon=ft.icons.CLOSE,on_click=lambda e: close_tab(e,tabs_control.selected_index)),
            create_input_field()
            ]))
            set_tab_name("NoteTab",tabs_control.selected_index)
            page.update()
            return new_tab
    
    def set_tab_name(name, index):
            # Ensure index is an integer
            if not isinstance(index, int):
                raise ValueError("Index must be an integer")

            if len(name) <= 0:
                name = "New Tab"
            elif 0 <= index < len(tab_names):
                tab_names.insert(index, name)
            else:
                # Handle the case where index is out of bounds, if needed
                print("Index is out of the valid range.")
            page.update()

    def name_current_tab(e,index):
        input = ft.TextField(on_submit=lambda e: set_tab_name(input, index))
        page.add()
        if 0 <= index < len(tabs_list)-1:
            tab_names[index] = input.value
    
    def add_tab(e):
            t = build_tab()
            
            if len(tabs_list)<=9:
                try:
                    tabs_list.append(t)  
                    tabs_control.tabs = tabs_list  
                    tabs_control.selected_index = len(tabs_list) - 1
                    page.update()
                except Exception as ex:
                    print("Something went wrong.")
            else:
                open_adaptive_dialog(e)
            page.update()
        
    def close_tab(e, index):
        if 0<= index < len(tabs_list):
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

    def close_app(event):
        print("exit")
        page.window_close()

    page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.NOTE_ADD, 
            on_click=add_tab, 
            bgcolor=ft.colors.GREY_800
        )

    # add_tab_button = ft.IconButton(
    #      ft.icons.ADD_TASK, 
    #      on_click=lambda e: add_tab(e, build_tab)
    #      )
    
    # close_app_button = ft.IconButton(
    #      ft.icons.CLOSE, 
    #      on_click=close_app,
    #      )
    
    # close_tab_button = ft.IconButton(
    #      ft.icons.CLOSE_OUTLINED, 
    #      on_click=lambda e: close_tab(e,tabs_control.selected_index),
    #      )
    
    page.appbar = ft.AppBar(leading=ft.PopupMenuButton(tooltip="Menu",icon=ft.icons.MENU,items=[
        ft.PopupMenuItem(),
        ft.PopupMenuItem(text="Connect API",on_click=print("CLICKED API BUTTON"),icon=ft.icons.API,),
        ft.PopupMenuItem(),        
        ft.PopupMenuItem(text="Connect AI",on_click=print("CLICKED AI BUTTON"),icon=ft.icons.SMART_BUTTON,),
        ft.PopupMenuItem(),        
        ft.PopupMenuItem(text="Preferences",on_click=print("CLICKED PREFERENCES BUTTON"),icon=ft.icons.SETTINGS,),
        ft.PopupMenuItem(),
        # ft.PopupMenuItem(text="Close All Tabs",checked=False,on_click=lambda e: close_tabs(e)),
        ]),
    leading_width=40,
    title=ft.WindowDragArea(
            ft.Container(
                ft.Text("SCRIBE"),
                padding=20
                )),
    center_title=True,
    bgcolor=ft.colors.SURFACE_VARIANT,
    actions=[ft.Row([
        ft.Divider(),
        ft.IconButton(ft.icons.APPS, on_click= lambda e: open_snackbar(e)),
        ft.Divider(),
        ft.IconButton(ft.icons.CLOSE,on_click=close_app),
        ft.Divider(),
        ft.Text("V1.1.27",tooltip="by Christian Paustell"),
        
        ft.Divider(),
        ])
        # This is where we can add another popup menu button
        ],
        )

    page.add(ft.Container(tabs_control, padding=10))

ft.app(target=main)