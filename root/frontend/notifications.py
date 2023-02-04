import flet as ft



class AlertCard(ft.UserControl):
    def __init__(self, alert, page):
        # self.page.session =
        super().__init__()
        self.alert = alert
        self.page = page

    def build(self):


        alert_card_stack = ft.Stack(data=self.alert.get('alertID'))


        alert_card = ft.Container(height=130, width=500, bgcolor='#DEFFFD', border_radius=ft.border_radius.all(20),
                                  alignment=ft.alignment.center)

        content_col = ft.Column(spacing=0)
        alert_card.content = content_col

        content_row = ft.Row()
        content_col.controls.append(content_row)

        image_slot = ft.Stack(controls=[

            ft.Container(expand=True, width=80, height=60, border_radius=ft.border_radius.all(100),
                         alignment=ft.alignment.center, margin=ft.margin.only(top=20, left=10),
                         content=ft.Container(width=60, height=60, bgcolor=ft.colors.RED,
                                              border_radius=ft.border_radius.all(100),
                                              alignment=ft.alignment.center_right))])

        content_row.controls.append(image_slot)

        message = ft.Container(width=400, content=ft.Container(alignment=ft.alignment.center_left,
                                                               content=ft.Text(value=self.alert.get("message"),
                                                                               color=ft.colors.BLACK,
                                                                               style=ft.TextThemeStyle.BODY_LARGE)))
        username = ft.Container(width=225, content=ft.Container(alignment=ft.alignment.center_left,
                                                                content=ft.Text(value=self.alert.get("from_username"),
                                                                                color=ft.colors.BLACK, weight='w300',
                                                                                style=ft.TextThemeStyle.LABEL_SMALL)))
        alert_info = ft.Column(spacing=4, controls=[message, username])
        content_row.controls.append(alert_info)
        alert_card_stack.controls.append(alert_card)

        response_row = ft.Row(alignment=ft.MainAxisAlignment('end'), spacing=10)
        content_col.controls.append(response_row)

        sub_message = ft.Container(content=ft.Container(alignment=ft.alignment.center_left,
                                                        content=ft.Text(value=self.alert.get("action_label"),
                                                                        color=ft.colors.BLACK,
                                                                        style=ft.TextThemeStyle.TITLE_SMALL)))
        self.approve_btn = ft.ElevatedButton(width=95, height=35, color=ft.colors.BLACK, bgcolor=ft.colors.LIGHT_BLUE_50, data='APPROVE',
                                        content=ft.Row(spacing=4, controls=[ft.Text('Accept', size=12),
                                                                            ft.Icon(ft.icons.THUMB_UP,
                                                                                    color=ft.colors.LIGHT_GREEN_600)]))
        self.deny_btn = ft.Container(data=self.alert.get('alertID'), margin=ft.margin.only(right=20),
                                content=ft.ElevatedButton(width=95, height=35, color=ft.colors.BLACK, data='DENY',
                                                          bgcolor=ft.colors.RED_50, content=ft.Row(spacing=4, controls=[
                                        ft.Text('DENY', size=12),
                                        ft.Icon(ft.icons.THUMB_DOWN, color=ft.colors.RED_400)])))
        response_row.controls.append(sub_message)
        response_row.controls.append(self.approve_btn)
        response_row.controls.append(self.deny_btn)

        return alert_card_stack
