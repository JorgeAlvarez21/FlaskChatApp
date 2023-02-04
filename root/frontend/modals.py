import flet as ft



class ModalWrapper(ft.UserControl):
	def build(self):
		_modal_wrapper = ft.Stack(
			controls=[
				ft.Container(
					expand=True,
					bgcolor=ft.colors.BLACK,
					opacity=0.3,
				)
			]
		)
		return _modal_wrapper

class CustomModalSm(ft.UserControl):
	def build(self):
		_gradient1 = '#ffffff'
		_gradient2 = '#d2d2d2'
		
		modal = ft.Container(
			border_radius=ft.border_radius.all(30),
			padding=ft.padding.only(left=40, top=25, right=40),
			width=550,
			height=450,
			offset=ft.transform.Offset(.7, 0.4),
			gradient=ft.LinearGradient(
				begin=ft.alignment.top_left,
				end=ft.alignment.bottom_right,
				colors=[_gradient1, _gradient2],
			)
		)
		return modal


class CustomModalMd(ft.UserControl):
	def build(self):
		_custom_modal = ft.Container(
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
		return _custom_modal
