import flet as ft
import flet as ft
from flet import (
	Column,
	Container,
	Text,
	Row,
	colors,
	TextField,
	AlertDialog,
)


class TestComponent(ft.UserControl):
	def __init__(self, page):
		super().__init__()
		self.page = page

	def build(self):
		dlg = AlertDialog(
			title=Text("请输入数字"), on_dismiss=lambda e: print("Dialog dismissed!")
		)  # 弹出对话框
		
		def open_dlg(e):
			"""打开对话框"""
			
			self.page.dialog = dlg
			dlg.open = True
			
			self.page.update()
			print("执行！")
		
		def textbox_changed(e):
			"""输入框TextFiled改变触发"""
			try:
				float(e.control.value)
			except ValueError:
				open_dlg(e)
		
		return Column(
			[
				Row(
					[
						Container(
							content=Column(
								[
									Text("参数设置", size=16),
									TextField(
										label="额定电流",
										height=200,
										color=ft.colors.BLACK,
										on_change=textbox_changed,
									),  # 文本输入框
									TextField(
										label="Some Label",
										height=100,
										on_change=textbox_changed,
										
									),  # 文本输入框
								],
							),
							width=400,
							height=500,
							padding=5,
							border_radius=5,
							bgcolor=colors.BLUE_100)
					]
				),
			
			]
		)
