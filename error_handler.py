import flet as ft

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