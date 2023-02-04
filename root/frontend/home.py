import datetime as dt
import json
import flet as ft
import requests
import sys
import path
import json
import time
import email
import random


directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent.parent)
import root.settings as settings
from notifications import AlertCard

input_text = None


class HomeViewControl(ft.UserControl):
	def __init__(self, page):
		super().__init__()
		self.page = page
		self._username = self.page.session.get("username")
		self._userID = self.page.session.get("userID")
		self._fullname = self.page.session.get("fullname")
		self._email = self.page.session.get("email")
		self._avatar = '/media/random_avatar1.png'
		self.conv_plane_name = ""
		# Temporary avatars for displaying on users added
		self._avatar_list = [f'/media/random_avatar{x}.png' for x in range(2, 9)]
		self._contact_avatars = {}
		self._contacts = self.user_contacts_loader()

	def user_contacts_loader(self):
		data = {"userID": self._userID}
		api_request = requests.get(
			f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/data/user/get_contacts", json=data)
		if api_request.status_code == 201:
			context = json.loads(api_request.content)
		elif api_request.status_code == 400:
			context = {}

		for contact in context.values():
			if contact['status'] == 'friends':
				self._contact_avatars[contact['contact_userID']] = random.choice(self._avatar_list)
		return context



	def build(self):
		# Colors

		# Fonts
		_font_main_color = '#000000'

		# Sidebar colors
		_sidebar_color = '#131737'
		_side_icons_color = '#ffffff'
		_active_side_icon_color = '#FF3D35'

		# Upper bar colors

		_upper_bar_color1 = '#f8f8f8'
		_upper_bar_color2 = '#4457c6'

		# Menu colors
		# _menu_color = ft.colors.BLUE_GREY_50

		_contact_c_before_color = '#9da8e1'
		_contact_c_after_color = '#7a83b6'
		_contact_c_lt_color = '#000000'
		_pinned_card_color = '#ffffff'
		_group_card_color = '#9da8e1'
		_menu_lt_color = '#000000'
		_search_box_color = '#e1e1e1'
		_search_icon_color = '#000000'
		_search_text_color = '#000000'
		_search_bgcolor = '#479196'
		_search_selected_color = "#BBCCC9"
		_expandable_color = '#ffffff'
		_menu_color = '#f8f8f8'


		# Chat screen colors
		_chat_color = '#ffffff'
		_text_box_color = '#ebebeb'
		_text_icons_color = '#000000'
		_send_btn_color = '#4457c6'
		_send_btn_hov_color = '#767797'
		_send_icon_color = '#cfcfcf'
		_msg_content_lt_color = '#000000'
		_msg_content_hint_color = '#000000'

		_landing_page_color = '#ffffff'

		# Modal Colors
		_btn_fr_added_color = '#37db59'
		_btn_not_added_color = '#9e6efe'
		_btn_pending_color = '#feac3c'
		_inactive_c_icon_color = '#1b3638'
		_active_c_icon_color = '#f67521'

		# Modals
		_modal_lg_gradient1 = '#ffffff'
		_modal_lg_gradient2 = '#c0d1e0'

		_modal_md_gradient1 = '#ffffff'
		_modal_md_gradient2 = '#c0d1e0'

		_contact_card_color = '#e2efef'

		# References
		pinned_ref = ft.Ref[ft.Column]()
		groups_ref = ft.Ref[ft.Column]()
		user_alerts_ref = ft.Ref[ft.Column]()
		conv_plane = ft.Ref[ft.Column]()
		text_box = ft.Ref[ft.Container]()
		outer_text_box = ft.Ref[ft.Container]()

		chat_screen_main = ft.Ref[ft.Container]()
		default_icon = ft.Ref[ft.IconButton]()
		recents_icon = ft.Ref[ft.IconButton]()
		favorites_icon = ft.Ref[ft.IconButton]()
		inbox_contacts_cards = ft.Ref[ft.Column]()
		arrow_down_pinned = ft.Ref[ft.Container]()
		arrow_down_groups = ft.Ref[ft.Container]()
		inbox_container = ft.Ref[ft.Container]()
		conv_plane_placeholder = ft.Ref[ft.Text]()
		notification_icon = ft.Ref[ft.IconButton]()

		# ************************************      FUNCTIONS          ************************************



		def _load_notifications():
			data = {"userID": self.page.session.get('userID')}
			api_request = requests.get(
				f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/alerts/fetch_by_user", json=data
			)
			if api_request.status_code == 201:
				context = json.loads(api_request.content)
				if context:
					notification_icon.current.icon == ft.icons.NOTIFICATION_ADD
					notification_icon.current.update()
				else:
					notification_icon.current.icon == ft.icons.NOTIFICATIONS
					notification_icon.current.update()
				return context
			else:
				return {}

		def logout_event(e):
						self.page.route = '/logout'
						self.page.go(self.page.route)
						self.page.update()

		def expand_pinned(e):
			if pinned_ref.current.height == 0:
				pinned_ref.current.height = 145
				arrow_down_pinned.current.visible = False
			else:
				pinned_ref.current.height = 0
				arrow_down_pinned.current.visible = True
			arrow_down_pinned.current.update()
			pinned_ref.current.update()

		def expand_groups(e):
			if groups_ref.current.height == 0:
				groups_ref.current.height = 145
				arrow_down_groups.current.visible = False

			else:
				groups_ref.current.height = 0
				arrow_down_groups.current.visible = True
			arrow_down_groups.current.update()
			groups_ref.current.update()

		def post_message(e):
			global input_text
			input_text = msg_content.value
			groupID, contact_userID = conv_plane.current.data['groupID'], conv_plane.current.data['contact_userID'],

			data = {'groupID':groupID, 'this_userID':self._userID, 'other_userID':contact_userID, 'message':input_text}
			post_message = requests.post(f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/inbox/messages/send",
			                             json=data)
			if post_message.status_code == 201:

				msg_content.value = ""
				msg_content.update()
				main_controller(e=None, on_post=contact_userID)
			else:
				print('Error Sending Message')

		def dismiss_modal(e):
			self.page.dialog.open = False
			_modal_wrapper.visible = False
			self.page.update()

		def dismiss_modal_alerts(e):
			self.page.dialog.open = False
			_modal_wrapper_alerts.visible = False
			self.page.update()

		def send_friend_request(e):
			data = {"this_userID": self.page.session.get('userID'),
			        "other_userID": e.control.data}
			api_request = requests.post(
				f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/requests/add_user", json=data)

			if api_request.status_code == 201:
				for card in _contacts_content.controls:
					button = card.content.controls[-1]
					button.bgcolor = _btn_pending_color
					button.text = 'Sent'
					button.update()


			elif api_request.content == b'Request Already Sent':
				data = {'userID': self.page.session.get('userID'), 'contact_userID': e.control.data}
				redo_add_request = requests.put(
					f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/requests/undo_add_user", json=data)

				if redo_add_request.status_code == 200:
					for card in _contacts_content.controls:
						button = card.content.controls[-1]
						button.bgcolor = _btn_not_added_color
						button.text = 'Add User'
						button.update()

		def send_add_fr_response(e, id_data):
			data = {'response': e.control.data, 'alertID': id_data}
			api_request = requests.put(
				f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/responses/friendship-status", json=data)
			if api_request.status_code == 200:
				user_alerts_ref.current.controls.clear()
				user_alerts_ref.current.update()
			self._contacts = self.user_contacts_loader()
			update_inbox_contacts()

		def update_inbox_contacts():
			if len(inbox_contacts_cards.current.controls) >= 1:
				inbox_contacts_cards.current.controls.clear()
			updated_cards = create_inbox_contacts()
			inbox_contacts_cards.current.controls.extend(updated_cards)
			inbox_contacts_cards.current.update()

			inbox_container.current.update()
			self.page.update()

		def fetch_user_data(username=None, userID=None):
			if not any([username, userID]):
				raise LookupError('Provide unique user credentials: username or userID')
			if username:
				data = {'username': username}
			else:
				data = {'userID': userID}

			api_request = requests.get(f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/data/user/get_data",
				json=data)
			if api_request.status_code == 201:
				user_data = json.loads(api_request.content)
				return user_data
			else:
				raise ValueError('http request was unsuccessful')

		def c_modal_view_default():
			items = []
			friends_dict = self._contacts
			for contact in friends_dict.values():
				if contact.get('status') == 'friends':
					data = {'userID': contact.get('contact_userID')}
					api_request = requests.get(
						f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/data/user/get_data", json=data
					)
					contact_info = json.loads(api_request.content)
					other_userID = contact_info.get('userID')
					other_username = contact_info.get('username')
					other_fullname = contact_info.get('fullname')

					card = ft.Container(
						data=contact.get('contact_userID'),
						alignment=ft.alignment.center,
						height=90,
						width=430,
						bgcolor=_contact_card_color,
						border_radius=ft.border_radius.all(20),
						border=ft.border.all(1, ft.colors.BLACK),
						content=ft.Row(
							alignment=ft.MainAxisAlignment('spaceEvenly'),
							controls=[
								ft.Container(
									width=50,
									height=50,
									border_radius=ft.border_radius.all(100),
									content=ft.Image(self._contact_avatars[contact.get('contact_userID')], border_radius=ft.border_radius.all(100)),

								),
								ft.Column(
									horizontal_alignment=ft.CrossAxisAlignment(
										"center"
									),
									alignment=ft.MainAxisAlignment('center'),
									controls=[ft.Text(other_fullname), ft.Text(other_username)],
								),
								ft.ElevatedButton(
									text='Friend',
									width=100,
									bgcolor=_contact_c_before_color,
									color='black',
									disabled=True,
									on_click=send_friend_request,
									data=other_userID,

								),
							]
						),
					)
					items.append(card)

			return items

		def c_modal_view_searched(search_userID):
			data = {"input": search_userID}
			api_request = requests.get(
				f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/data/find_user",
				json=data,
			)

			if api_request.status_code == 201:
				d_result = json.loads(api_request.content)
				for i in range(1, int((len(d_result) / 3) + 1)):
					other_fullname = d_result["fullname" + str(i)]
					other_username = d_result["username" + str(i)]
					other_userID = d_result["userID" + str(i)]
					if other_userID != self.page.session.get('userID'):

						btn_bgcolor = _btn_not_added_color
						btn_text = 'Add User'
						btn_is_disabled = False

						friends_dict = self._contacts
						for i, _dict in friends_dict.items():
							contact = _dict.get('contact_userID')
							if other_userID == contact:
								status = _dict['status']
								if status == 'pending':
									btn_bgcolor = _btn_pending_color
									btn_text = 'Sent'

								elif status == 'friends':
									btn_text = 'Friend'
									btn_bgcolor = _contact_c_before_color
									btn_is_disabled = True
					else:
						return None

					card = ft.Container(
						data=other_userID,

						alignment=ft.alignment.center,
						height=90,
						width=430,
						bgcolor=_contact_card_color,
						border_radius=ft.border_radius.all(20),
						border=ft.border.all(1, ft.colors.BLACK),
						content=ft.Row(
							alignment=ft.MainAxisAlignment('spaceEvenly'),
							controls=[
								ft.Container(
									width=50,
									height=50,
									bgcolor=ft.colors.BLUE_GREY_600,
									border_radius=ft.border_radius.all(100),
								),
								ft.Column(
									horizontal_alignment=ft.CrossAxisAlignment(
										"center"
									),
									alignment=ft.MainAxisAlignment('center'),
									controls=[ft.Text(other_fullname), ft.Text(other_username)],
								),
								ft.ElevatedButton(
									text=btn_text,
									width=100,
									bgcolor=btn_bgcolor,
									color=_font_main_color,
									disabled=btn_is_disabled,
									on_click=send_friend_request,
									data=other_userID,

								),
							]
						),
					)
					items = [card]
					return items
			else:
				print("login failed from login flet")

		def c_modal_view_recents():
			items = []
			for i in range(3):
				card = ft.Container(
					alignment=ft.alignment.center,
					height=90,
					width=430,
					border_radius=ft.border_radius.all(30),
					border=ft.border.all(1, ft.colors.BLACK),
					bgcolor=_contact_card_color,
					content=ft.Row(
						alignment=ft.MainAxisAlignment('spaceEvenly'),
						controls=[
							ft.Container(
								width=50,
								height=50,
								bgcolor=ft.colors.BLUE_GREY_600,
								border_radius=ft.border_radius.all(100),
								content=ft.Text('Recents')
							),
							ft.Column(
								horizontal_alignment=ft.CrossAxisAlignment(
									"center"
								),
								alignment=ft.MainAxisAlignment('center')
							),
							ft.ElevatedButton(
								text='Friend',
								width=100,
								bgcolor=_contact_c_before_color,
								color='black',
								disabled=True,

							),
						]
					),
				)
				items.append(card)
			return items

		def c_modal_view_favorites():
			items = []
			for i in range(3):
				card = ft.Container(
					alignment=ft.alignment.center,
					height=90,
					width=430,
					border_radius=ft.border_radius.all(20),
					border=ft.border.all(1, ft.colors.BLACK),
					bgcolor=_contact_card_color,
					content=ft.Row(
						alignment=ft.MainAxisAlignment('spaceEvenly'),
						controls=[
							ft.Container(
								width=50,
								height=50,
								bgcolor=ft.colors.BLUE_GREY_600,
								border_radius=ft.border_radius.all(100),
								content=ft.Text('Favorites')
							),
							ft.Column(
								horizontal_alignment=ft.CrossAxisAlignment(
									"center"
								),
								alignment=ft.MainAxisAlignment('center')
							),
							ft.ElevatedButton(
								text='Friend',
								width=100,
								bgcolor=_contact_c_before_color,
								color='black',
								disabled=True,

							),
						]
					),
				)
				items.append(card)
			return items

		def contacts_modal(e):
			# Clean Wrapper and Content
			if len(_modal_wrapper.controls) > 1:
				_modal_wrapper.controls.pop()
			if len(_contacts_content.controls) >= 1:
				_contacts_content.controls.clear()
				# _contacts_content.update()

			show_view = e.control.data
			_modal_wrapper.controls.append(_custom_modal_lg)
			_custom_modal_lg.content = _contacts_base

			self.page.dialog = _modal_wrapper

			if show_view == 'Search':
				search_contact = e.control.value
				_display_modal = c_modal_view_searched(search_contact)
				e.control.value = ''
				e.control.update()

			if show_view == 'Recents':
				_display_modal = c_modal_view_recents()
				recents_icon.current.icon_color = _active_c_icon_color
			else:
				if not recents_icon.current.icon_color == _inactive_c_icon_color:
					recents_icon.current.icon_color = _inactive_c_icon_color

			if show_view == 'Favorites':
				_display_modal = c_modal_view_favorites()
				favorites_icon.current.icon_color = _active_c_icon_color

			else:
				if not favorites_icon.current.icon_color == _inactive_c_icon_color:
					favorites_icon.current.icon_color = _inactive_c_icon_color

			if show_view not in ['Search', 'Favorites', 'Recents']:
				_display_modal = c_modal_view_default()
				default_icon.current.icon_color = _active_c_icon_color
			else:
				if not default_icon.current.icon_color == _inactive_c_icon_color:
					default_icon.current.icon_color = _inactive_c_icon_color

			if _display_modal and isinstance(_display_modal, list):
				_contacts_content.controls.extend(_display_modal)
			self.page.dialog.open = True
			_modal_wrapper.visible = True
			self.page.update()

			default_icon.current.update()
			default_icon.current.update()
			favorites_icon.current.update()
			recents_icon.current.update()

		def notifications_modal_open(e):
			notifications_list = _load_notifications()
			for alert in notifications_list.values():
				if alert.get('status') == 'open':
					alert_card = AlertCard(alert, self.page).build()
					approve_btn = alert_card.controls[0].content.controls[-1].controls[-2]
					deny_btn = alert_card.controls[0].content.controls[-1].controls[-1].content
					alertID = alert_card.controls[0].content.controls[-1].controls[-1].data

					approve_btn.on_click = lambda e: send_add_fr_response(e, id_data=alertID)
					deny_btn.on_click = lambda e: send_add_fr_response(e, id_data=alertID)
					user_alerts_ref.current.controls.append(alert_card)

			if len(_modal_wrapper_alerts.controls) > 1:
				_modal_wrapper_alerts.controls.pop()
			self.page.dialog = _modal_wrapper_alerts
			_modal_wrapper_alerts.controls.append(_custom_modal_md)
			_custom_modal_md.content = _notifications_card
			self.page.dialog.open = True
			_modal_wrapper_alerts.visible = True
			self.page.update()

		def chat_default_view():
			default = ft.Container(width=600, height=500, padding=ft.padding.only(
				left=50),
			                       content=ft.Column(controls=[
				                       ft.Container(alignment=ft.alignment.top_left, margin=ft.margin.only(top=30),
				                                    content=ft.Text(
					                                    'Welcome', weight='w500', color=_sidebar_color,
					                                    style=ft.TextThemeStyle.DISPLAY_MEDIUM)),

				                       ft.Container(
					                       alignment=ft.alignment.top_left, margin=ft.margin.only(top=20),
					                       content=ft.Text(
						                       'Chat Messaging', color=ft.colors.BLACK87, weight='w500',
						                       style=ft.TextThemeStyle.TITLE_LARGE, width=500)),

				                       ft.Container(
					                       alignment=ft.alignment.center, margin=ft.margin.only(top=10),
					                       content=ft.Text(
						                       'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
						                       'sed do eiusmod tempor '
						                       'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
						                       'quis nostrud '
						                       'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
						                       style=ft.TextThemeStyle.TITLE_MEDIUM, width=400)),

				                       ft.Container(
					                       alignment=ft.alignment.top_left, margin=ft.margin.only(top=60),
					                       content=ft.Text(
						                       'Lorem lorem lorem lorem lorem more more lorem', color=ft.colors.BLACK87,
						                       weight='w500',
						                       style=ft.TextThemeStyle.TITLE_LARGE, width=400)),

				                       ft.Container(
					                       alignment=ft.alignment.center, margin=ft.margin.only(top=10),
					                       content=ft.Text(
						                       'Lorem ipsum dolor sit amet, consectetur.',
						                       style=ft.TextThemeStyle.TITLE_MEDIUM, width=400)),
				                       ft.Container(
					                       alignment=ft.alignment.top_left, margin=ft.margin.only(top=60),
					                       content=ft.Text(
						                       'Click to learn more.',
						                       style=ft.TextThemeStyle.TITLE_SMALL, width=400)),
				                       ft.Container(
					                       alignment=ft.alignment.top_left, margin=ft.margin.only(top=10),
					                       content=ft.ElevatedButton('Go to site', width=120, style=ft.ButtonStyle(
						                       bgcolor={
							                       '': ft.colors.DEEP_ORANGE}),
					                                                 )),
			                       ]))
			return default

		def received_inbox_card(msg_text, timestamp, contact_userID, username, fullname, email, image):

			if isinstance(msg_text, str):
				add_space = len(msg_text)/42
				box_height = 110 + add_space*(21)
				msg_card = ft.Container(height=box_height,
				                        alignment=ft.alignment.top_right,
					content=
					ft.Container(bgcolor='#fbf5fa', border_radius=ft.border_radius.all(30), padding=ft.padding.all(13),
					             alignment=ft.alignment.top_left, width=400, height=box_height-21,
					             content=ft.Container(
					content=ft.Row(
						alignment=ft.MainAxisAlignment('start'),
						controls=[
							ft.Container(
								padding=ft.padding.only(left=10),
								content=ft.Container(
									height=30,
									content=ft.Column(
										horizontal_alignment=ft.CrossAxisAlignment('start'),
										spacing=3,
										controls=[
											ft.Container(
												margin=ft.margin.only(right=10),
												width=250, content=ft.Row(
												spacing=7,
												controls=[# Time

													ft.Container(margin=ft.margin.only(top=5),
														content=ft.Text(timestamp, size=11,
															color=ft.colors.BLUE_GREY_300, )),
													ft.Container(
														alignment = ft.alignment.top_right,
														content=ft.Text(
															username, style=ft.TextThemeStyle.TITLE_MEDIUM
														)
													),  # Name
												],
											)),

											ft.Container(width=300,
												margin=ft.margin.only(top=10),
												content=ft.Text(msg_text, size=14, color=ft.colors.BLACK),
											),  # Message Content
										]
									),
								),
							),
							ft.Container(
								content=ft.Image(src=image, width=45, height=45,
									border_radius=ft.border_radius.all(100))),
						]
					))),
				)
				return msg_card
			else:
				return None

		def sent_inbox_card(msg_text, timestamp, username):

			if msg_text:

				add_space = len(msg_text)/42
				box_height = 110 + add_space*(21)
				msg_card = ft.Container(height=box_height,
				                        alignment=ft.alignment.top_left,
					content=
					ft.Container(bgcolor='#ebfaff', border_radius=ft.border_radius.all(30), padding=ft.padding.all(13),
					             alignment=ft.alignment.top_left, width=400, height=box_height-21,
					             content=ft.Container(
					content=ft.Row(
						alignment=ft.MainAxisAlignment('start'),
						controls=[
							ft.Container(
								content=ft.Image(src=self._avatar, width=45, height=45,
									border_radius=ft.border_radius.all(100))),
							ft.Container(
								padding=ft.padding.only(left=10),
								content=ft.Container(
									height=30,
									content=ft.Column(
										horizontal_alignment=ft.CrossAxisAlignment('start'),
										spacing=3,
										controls=[
											ft.Container(
												margin=ft.margin.only(right=10),
												width=250, content=ft.Row(
												spacing=7,
												controls=[# Time

													ft.Container(
														alignment = ft.alignment.top_right,
														content=ft.Text(
															username, style=ft.TextThemeStyle.TITLE_MEDIUM
														)
													),  # Name
													ft.Container(margin=ft.margin.only(top=5),
														content=ft.Text(timestamp, size=11,
															color=ft.colors.BLUE_GREY_300, )),
												],
											)),

											ft.Container(width=300,
												margin=ft.margin.only(top=10),
												content=ft.Text(msg_text, size=14, color=ft.colors.BLACK),
											),  # Message Content
										]
									),
								),
							),
						]
					))),
				)
				return msg_card

		def create_inbox_contacts():
			items = []
			friends_dict = self._contacts
			time.sleep(.2)
			for k, _dict in friends_dict.items():
				contact_userID = _dict['contact_userID']
				status = _dict['status']
				if status == 'friends':
					contact = fetch_user_data(userID= contact_userID)
					name = contact['fullname']
					image = self._contact_avatars[contact_userID]
					card = ft.ElevatedButton(
			                  style=ft.ButtonStyle(
				                  bgcolor={
					                  "hovered": _contact_c_after_color,
					                  "": _contact_c_before_color,
				                  },
				                  shape={
					                  "": ft.buttons.RoundedRectangleBorder(
						                  radius=30),
				                  },

			                  ),
			                  content=ft.Container(
				                  data=contact_userID,
				                  on_click=main_controller,
				                  width=270,
				                  height=75,
				                  border_radius=ft.border_radius.all(
					                  15
				                  ),
				                  content=ft.Row(
					                  alignment="start",
					                  spacing=5,
					                  controls=[
						                  ft.Container(
							                  width=45,
							                  height=45,
							                  content=ft.Image(
								                  src=image,
								                  height=50,
								                  width=50,
								                  border_radius=ft.border_radius.all(
									                  100
								                  ),
							                  ),
						                  ),
						                  ft.Container(
							                  padding=ft.padding.only(
								                  top=14
							                  ),
							                  width=160,
							                  height=60,
							                  margin=ft.margin.all(
								                  0
							                  ),
							                  content=ft.Text(
								                  name,
								                  size=14,
								                  color=_contact_c_lt_color
							                  ),
						                  ),
						                  ft.Container(
							                  height=50,
							                  content=ft.Column(
								                  horizontal_alignment="center",
								                  controls=[
									                  ft.Container(
										                  width=50,
										                  margin=ft.margin.only(
											                  right=55
										                  ),
										                  content=ft.Column(expand=True,
										                                    horizontal_alignment=ft.CrossAxisAlignment(
											                  'center'),
											                  controls=[
										                  ft.Text(
											                  "7:21 PM",
											                  size=12,
											                  color=_contact_c_lt_color

										                  ),
									                  ft.Icon(
										                  name=ft.icons.CHECK_CIRCLE_ROUNDED,
										                  color=ft.colors.GREEN_300,
										                  size=20,
									                  )])),
								                  ],
							                  ),
						                  ),
					                  ],
				                  ),
			                  ),
		                  )
					items.append(card)
			return items

		def conversation_loader(contact_userID, username, fullname, email):
			data = {"userID": self._userID,
			        "contact_userID": contact_userID}
			contact_user_data = fetch_user_data(userID=contact_userID)

			username = contact_user_data.get('username')
			fullname = contact_user_data.get('fullname')
			email = contact_user_data.get('email')

			api_request = requests.get(
				f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/inbox/data/fetch_all", json=data)

			if api_request.status_code == 201:
				inbox_log = json.loads(api_request.content)

				box = ft.Column(controls=[])
				for card in inbox_log:
					if card['msg_content'] != 'null' and card['sent_by_one'] != 'null':
						is_user_one = True if card['userID_one'] == self._userID else False
						if is_user_one:
							is_msg_sender = True if card['sent_by_one'] == 'true' else False
						else:
							is_msg_sender = False if card['sent_by_one'] == 'true' else True

						if is_msg_sender:

							build_card = sent_inbox_card(msg_text=card['msg_content'], timestamp=card[
								'timestamp_sent'], username=self._username)
						else:
							build_card = received_inbox_card(msg_text=card['msg_content'], timestamp=card[
								'timestamp_sent'], contact_userID=contact_userID, username=username,
							                                 fullname=fullname, email=email, image=self._contact_avatars[contact_userID])

						conv_plane.current.data = {'groupID': inbox_log[0]['groupID'],
						                           'contact_userID': contact_userID}
						conv_plane.current.update()
						if build_card is not None:
							box.controls.append(build_card)
				return box
			else:
				raise ValueError('Unable to load this user\'s inbox')

		def main_controller(e, on_post=None):
			if on_post:
				contact_userID = on_post
			else:
				contact_userID = e.control.data

			if len(conv_plane.current.controls) >= 1:
				conv_plane.current.controls.clear()
			if not contact_userID:
				chat_screen_main.current.bgcolor = _landing_page_color
				text_box.current.visible = False
				chat_screen_main.current.update()
				text_box.current.update()
				default_view = chat_default_view()
				conv_plane.current.controls.append(default_view)
				conv_plane.current.update()
			else:

				contact_user_data = fetch_user_data(userID=contact_userID)

				username = contact_user_data.get('username')
				fullname = contact_user_data.get('fullname')
				email = contact_user_data.get('email')


				chat_screen_main.current.bgcolor = _chat_color
				outer_text_box.current.visible = True
				chat_screen_main.current.update()
				text_box.current.visible = True
				text_box.current.update()
				chat_context = conversation_loader(contact_userID, username, fullname, email)
				conv_plane.current.controls.append(chat_context)
				conv_plane.current.update()

				self.conv_plane_name =fullname
				conv_plane_placeholder.current.value = self.conv_plane_name
				conv_plane_placeholder.current.update()


		_custom_modal_md = ft.Container(
			border_radius=ft.border_radius.all(30),
			padding=ft.padding.only(left=40, top=25, right=40),
			width=550,
			height=450,
			offset=ft.transform.Offset(.7, 0.4),
			gradient=ft.LinearGradient(
				begin=ft.alignment.top_left,
				end=ft.alignment.bottom_right,
				colors=[_modal_md_gradient1, _modal_md_gradient2],
			),
		)

		_custom_modal_lg = ft.Container(
			border_radius=ft.border_radius.all(30),
			padding=ft.padding.only(left=40, top=25, right=40),
			width=650,
			height=550,
			offset=ft.transform.Offset(.5, 0.3),
			gradient=ft.LinearGradient(
				begin=ft.alignment.top_left,
				end=ft.alignment.bottom_right,
				colors=[_modal_lg_gradient1, _modal_lg_gradient2],
			),
		)

		_contacts_content = ft.Column(
			spacing=16,
			scroll=True,
			horizontal_alignment=ft.CrossAxisAlignment("center")
		)

		_contacts_base = ft.Column(
			expand=True,
			controls=[
				ft.Container(bgcolor=ft.colors.WHITE, content=
				ft.TextField(
					value=None,
					color=ft.colors.BLACK,
					data='Search',
					label="Search Friends",
					height=45,
					on_submit=contacts_modal
				)),
				ft.Row(
					alignment=ft.MainAxisAlignment("spaceEvenly"),
					controls=[
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.PUNCH_CLOCK, data='Recents', ref=recents_icon,
								              icon_color=_inactive_c_icon_color, on_click=contacts_modal),
								ft.Text("Recents"),
							],
						),
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.CONTACTS, ref=default_icon, data='Default',
								              icon_color=_inactive_c_icon_color,
								              on_click=contacts_modal),
								ft.Text("Contacts"),
							],
						),
						ft.Column(
							spacing=0,
							horizontal_alignment=ft.CrossAxisAlignment("center"),
							controls=[
								ft.IconButton(ft.icons.STAR, data='Favorites', ref=favorites_icon,
								              icon_color=_inactive_c_icon_color,
								              on_click=contacts_modal, disabled=False
								              ),
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
					content=_contacts_content
				)
			],
		)

		_notifications_card = ft.Column(
			expand=True,
			controls=[
				ft.Text(
					"Notifcations", color=_sidebar_color, size=22, weight="w500"
				),
				ft.Column(ref=user_alerts_ref)
			],
		)

		_modal_wrapper = ft.Stack(
			controls=[
				ft.Container(
					expand=True,
					bgcolor=ft.colors.BLACK,
					on_click=dismiss_modal,
					opacity=0.5,
				)
			]
		)
		_modal_wrapper_alerts = ft.Stack(
			controls=[
				ft.Container(
					expand=True,
					bgcolor=ft.colors.BLACK,
					on_click=dismiss_modal_alerts,
					opacity=0.5,
				)
			]
		)

		msg_content = ft.TextField(hint_text="Write a message..", color=_msg_content_lt_color,
			hint_style=ft.TextStyle(color=_msg_content_hint_color), border_width=0, on_submit=post_message,
			capitalization="sentences")
		created_inbox_cards = create_inbox_contacts()
		main_content = ft.Row(
			alignment="center",
			spacing=0,
			controls=[

				ft.Column(
					controls=[
						ft.Container(
							border=ft.border.all(2, ft.colors.BLACK),
							border_radius=ft.border_radius.only(topRight=0, topLeft=30,
							                                    bottomLeft=30, bottomRight=0),


							bgcolor=_sidebar_color,
							content=ft.Column(
								controls=[
									ft.Container(
										width=45,
										height=794,
										content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment(
											"center"),
											alignment=ft.MainAxisAlignment("end"),
											controls=[
												ft.Container(
													margin=ft.margin.only(bottom=20),
													content=ft.IconButton(
														icon=ft.icons.PERSON,
														icon_color=_side_icons_color, icon_size=30,
														on_click=contacts_modal,
													),
												),
												ft.Container(

													margin=ft.margin.only(bottom=20),
													content=ft.IconButton(ref=notification_icon,
														icon=ft.icons.NOTIFICATIONS,
														icon_color=_side_icons_color,
														on_click=notifications_modal_open, icon_size=30,

													),
												),

												ft.Container(height=480),

												ft.Container(margin=ft.margin.only(bottom=20),
													content=ft.IconButton(icon=ft.icons.SETTINGS,
														icon_color=_side_icons_color, icon_size=30)),

												ft.Container(
													margin=ft.margin.only(bottom=20),
													content=ft.IconButton(
														icon=ft.icons.LOGOUT,
														icon_color=_side_icons_color, icon_size=30,
														on_click=logout_event,
													),
												),
											],
										),
									)
								],
							),
						)
					],
				),
				ft.Column(spacing=0, controls=[
					ft.Container(
						bgcolor=_upper_bar_color1,

						border=ft.border.only(top=ft.border.BorderSide(2, ft.colors.BLACK)),
						height=42,
						width=400,
						alignment=ft.alignment.center,
						margin=ft.margin.only(top=2),
						padding=ft.padding.only(
							left=10
						),
				         content=ft.Row(alignment=ft.MainAxisAlignment('start'), controls=[ft.Container(margin=ft.margin.only(left=20),
								content=ft.Image(src=self._avatar, width=30, height=30,
									border_radius=ft.border_radius.all(100))),
							 ft.Text(f"Hi {self.page.session.get('fullname')}!", size=14, weight="w400",
							color=ft.colors.BLACK)]),

					),
					ft.Container(

						border=ft.border.only(bottom=ft.border.BorderSide(2, ft.colors.BLACK)),
						width=400,
						content=ft.Column(
							height=756,
							scroll=ft.ScrollMode.HIDDEN,
							controls=[
								ft.Container(
									content=ft.Column(
										spacing=0,
										expand=True,
										controls=[
											ft.Container(
												bgcolor=_menu_color,
												content=ft.Container(margin=ft.margin.only(left=20, right=20),
													content=ft.Column(
														controls=[
															ft.Container(
																alignment=ft.alignment.center
															),
															# ft.Divider(opacity=0.5),
															ft.Container(


																content=ft.Row(controls=[ft.IconButton(
																	icon=ft.icons.ARROW_DROP_DOWN_CIRCLE,
																	on_click=expand_pinned,
																	icon_color='black', icon_size=25, ),
																	ft.Text(
																	"Pinned Messages",
																	size=16,
																	weight="w500",
																	color='black',
																)])
															),
															ft.Container(
																border=ft.border.only(
																	top=ft.border.BorderSide(1, ft.colors.BLACK),
																	bottom=ft.border.BorderSide(1, ft.colors.BLACK)),

																bgcolor=_expandable_color,
																content=ft.Column(ref=pinned_ref,
																                  height=0,
																                  scroll=True,
																                  controls=[
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_pinned_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_pinned_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_pinned_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_pinned_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																                  ],
																                  )
																					),
																					ft.Container(
																					             content=ft.Container(ref=arrow_down_pinned, width=500, height=60,
																					                                  content=ft.Image(
																						             'drop_arrow_down.jpg'
																						             )))


														]
													)
												),
											),
											ft.Container(
												bgcolor=_menu_color,
												content=ft.Container(
													content=ft.Column(
														controls=[
															ft.Container(
																padding=ft.padding.only(bottom=0, left=15),
																margin=ft.margin.all(0), content=ft.Row(controls=[
																	ft.IconButton(
																		icon=ft.icons.ARROW_DROP_DOWN_CIRCLE, on_click = expand_groups,
																		icon_color='black', icon_size=25),
																	ft.Text("Groups", size=16, weight="w500",
																		color='black', )])),

															ft.Container(margin=ft.margin.only(left=20, right=20),
																border=ft.border.only(
																	top=ft.border.BorderSide(1, ft.colors.BLACK),
																	bottom=ft.border.BorderSide(1, ft.colors.BLACK)),

																bgcolor=_expandable_color,
																content=ft.Column(ref=groups_ref,
																                  height=0,
																                  scroll=True,
																                  controls=[
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_group_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_group_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_group_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																	                  ft.Container(
																		                  height=58,
																		                  padding=ft.padding.only(
																			                  left=40,
																			                  right=40,
																		                  ),
																		                  content=ft.Container(
																			                  border_radius=ft.border_radius.all(
																				                  15
																			                  ),
																			                  bgcolor=_group_card_color,
																			                  expand=True,
																		                  ),
																	                  ),
																                  ],
																                  ),
															),

															ft.Container(
																content=ft.Container(ref=arrow_down_groups, width=500,
																                     height=60, content=ft.Image(
																		'drop_arrow_down.jpg'))),


														]
													)
												),
											),

											ft.Container(bgcolor=_menu_color,
												height=60,
											    padding=ft.padding.only(bottom=20),
												alignment=ft.alignment.center,
												content=ft.Container(bgcolor=ft.colors.WHITE,
												                     width=210, content=ft.TextField(
													prefix_icon=ft.icons.PERSON_SEARCH,
													label="Search Inbox",
													text_size=14,
													content_padding=ft.padding.only(
														top=3, left=8
													),
													border_radius=ft.border_radius.all(20),
													color=ft.colors.BLACK,
													text_style=ft.TextStyle(color=_search_text_color),
													label_style=ft.TextStyle(color=_search_text_color),
													selection_color=_search_selected_color,
													capitalization="sentences",
													# content=ft.Container(expand=True, bgcolor=_search_bgcolor, )

												)),
											),
											ft.Container(bgcolor=_menu_color,
											             content=
											             ft.Container(width=400,
												             margin=ft.margin.only(bottom=5, left=15),
												             content=ft.Text(
													             "Inbox",
													             size=20,
													             weight="w500",
													             color=_menu_lt_color, bgcolor=_menu_color
												             ),
											             )),

											ft.Container(
												bgcolor='#ffffff',
												margin=ft.margin.only(left=25, right=25, top=5),
												border_radius=ft.border_radius.all(15),

												border=ft.border.all(2, ft.colors.BLACK),
												alignment=ft.alignment.top_center,
												height=380,

												content=ft.Column(width=400,
													spacing=20,
												                  horizontal_alignment=ft.CrossAxisAlignment('center'),
												                  alignment=ft.MainAxisAlignment('center'),

												                  scroll=True,
												                  controls=
												                  [
													                  ft.Container(ref=inbox_container,
													                               margin=ft.margin.only(top=20),
														                  content=ft.Column(ref=inbox_contacts_cards,
															                  spacing=18,
															                                controls=created_inbox_cards
														                  )
													                  ),
												                  ],
												                  ),
											),
										],
									),
								)
							],
						))]
				          ),
				ft.Column(
					controls=[
						ft.Container(
							height=798,
							width=600,
							content=ft.Column(
								spacing=0,
								expand=True,
								controls=[
									ft.Container(
										height=40,
										border=ft.border.all(1, ft.colors.BLACK),
										border_radius=ft.border_radius.only(topRight=30, topLeft=0,
										                                    bottomLeft=0, bottomRight=0),
										alignment=ft.alignment.top_right,
										bgcolor=_upper_bar_color2,
										content=ft.Container(
											border_radius=ft.border_radius.all(20),
											content=ft.Row(alignment=ft.MainAxisAlignment('spaceBetween'),
											               controls=[ft.Container(margin=ft.margin.only(left=25),
											                                       content=ft.Text(
												                                              value=self.conv_plane_name,
											                                              ref=conv_plane_placeholder,
											                                 color=ft.colors.WHITE, size=16)),

											ft.Container(margin=ft.margin.only(right=20), content=ft.IconButton(
			icon=ft.icons.MENU, on_click=lambda e:update_inbox_contacts(),
											                                           icon_color='white'))])
										),
									),
									ft.Container(
										ref=chat_screen_main,
										border=ft.border.only(top=ft.border.BorderSide(2, ft.colors.BLACK),
										                      right=ft.border.BorderSide(2, ft.colors.BLACK),
										                      left=ft.border.BorderSide(2, ft.colors.BLACK),
										                      bottom=ft.border.BorderSide(2, ft.colors.BLACK)),
										border_radius=ft.border_radius.only(topRight=0, topLeft=0,
										                                    bottomLeft=0, bottomRight=30),

										expand=True,
										bgcolor=_landing_page_color,
										content=ft.Column(
											controls=[
												ft.Container(margin=ft.margin.only(top=25),
													height=500,
													content=ft.Column(
														alignment=ft.MainAxisAlignment('start'),
														ref=conv_plane,
														scroll=True,
														auto_scroll=True,
														controls=[chat_default_view()]
													),
												),
												ft.Container(
													ref=outer_text_box,
													visible=False,
													expand=True,
													margin=ft.margin.all(0),
													padding=ft.padding.only(
														bottom=20,
														left=15,
														right=15,
													),
													content=ft.Container(
														ref=text_box,
														bgcolor=_text_box_color,
														border=ft.border.all(2, ft.colors.BLACK),
														border_radius=ft.border_radius.all(
															25
														),
														padding=ft.padding.only(
															bottom=20
														),
														content=ft.Column(
															tight=True,
															spacing=0,
															controls=[
																ft.Container(
																	padding=ft.padding.only(
																		left=20,
																		right=30,
																		top=20,
																	),
																	content=ft.Container(
																		border_radius=ft.border_radius.all(
																			15
																		),
																		content=ft.Row(
																			controls=[
																				ft.Image(
																					src=self._avatar,
																					width=35,
																					height=35,
																					border_radius=ft.border_radius.all(
																						100
																					),
																				), msg_content

																			]
																		),
																	),
																),
																ft.Container(height=100,
																	content=ft.Row(
																		alignment="end",
																		spacing=0,
																		vertical_alignment="start",
																		controls=[
																			ft.Container(
																				padding=ft.padding.only(
																					top=62,
																				),
																				content=ft.IconButton(
																					ft.icons.ATTACHMENT,
																					icon_color=_text_icons_color,
																				),
																			),
																			ft.Container(
																				padding=ft.padding.only(
																					top=62,
																				),
																				content=ft.IconButton(
																					ft.icons.SHARE_OUTLINED,
																					icon_color=_text_icons_color,
																				),
																			),
																			ft.Container(
																				padding=ft.padding.only(
																					top=62,
																					right=10,
																				),
																				content=ft.IconButton(
																					ft.icons.TAG_FACES,
																					icon_color=_text_icons_color,
																				),
																			),
																			ft.Container(
																				padding=ft.padding.only(
																					right=20,
																					top=65,
																				),
																				width=115,
																				height=100,
																				content=ft.ElevatedButton(
																					on_click=post_message,
																					content=ft.Container(
																						content=ft.Icon(
																							name=ft.icons.SEND_SHARP,
																							color=_send_icon_color
																						),
																						width=30,
																					),
																					text="Send",
																					style=ft.ButtonStyle(
																						animation_duration=900,
																						shape=ft.BeveledRectangleBorder(
																							radius=8
																						),
																						color={
																							"": ft.colors.WHITE,
																							"hovered": ft.colors.BLACK,
																						},
																						bgcolor={
																							"": _send_btn_color,
																							"hovered": _send_btn_hov_color,
																						},
																						shadow_color={
																							"hovered": "#191C1F"
																						},
																						elevation={
																							"focused": 1
																						},
																						padding={
																							"hovered": 6
																						},
																					),
																				),
																			),
																		],
																	)
																),
															],
														),
													),
												),
											]
										),
									),
								],
							),
						)
					],
				),
			],
		)

		page_view = ft.Container(content=main_content)
		return page_view


