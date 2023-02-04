import flet as ft

class ContactsMenu(ft.UserControl):
	def build(self):

		_menu = ft.Column(
			expand=True,
			controls=[
				ft.TextField(
					label="Search Friends",
					height=45,
					color=ft.colors.BLACK,
					on_submit=search_contact_card,
				),
				ft.Row(
					alignment=ft.MainAxisAlignment("spaceEvenly"),
					controls=[
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.PUNCH_CLOCK),
								ft.Text("Recents"),
							],
						),
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.CONTACTS),
								ft.Text("Contacts"),
							],
						),
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.STAR, icon_color=ft.colors.YELLOW_ACCENT, icon_size=30),
								ft.Text("Favorites"),
							],
						),
					],
				),
				ft.Container(
					margin=ft.margin.only(top=20, bottom=15),
					height=180,
					expand=True,
					alignment=ft.alignment.top_center,
					content=ft.Column(
						ref=ref_found_contacts,
						spacing=16,
						scroll=True,
						horizontal_alignment=ft.CrossAxisAlignment("center")
						# Contact Card
						# ft.Container(margin=ft.margin.only(left=20, right=20),
						#              height=65, width=380,
						#              border_radius=ft.border_radius.all(20),
						#              bgcolor=ft.colors.BLUE_GREY_600, opacity=.3),
						# ft.Container(margin=ft.margin.only(left=20, right=20),
						#              height=65, width=380,
						#              border_radius=ft.border_radius.all(20),
						#              bgcolor=ft.colors.BLUE_GREY_600, opacity=.3),
						# ft.Container(margin=ft.margin.only(left=20, right=20),
						#              height=65, width=380,
						#              border_radius=ft.border_radius.all(20),
						#              bgcolor=ft.colors.BLUE_GREY_600, opacity=.3),
					),
				),
			],
		)
		return _menu
	
class NotificationstCard(ft.UserControl):
	def build(self):
		_notifications_card = ft.Column(
			expand=True,
			controls=[
				ft.Text(
					"Notifcations", color=ft.colors.RED_300, size=22, weight="w500"
				),
				ft.Divider(color=ft.colors.RED_300, thickness=2),
				ft.Column(ref=user_alerts_ref)
			],
		)
		return _notifications_card



