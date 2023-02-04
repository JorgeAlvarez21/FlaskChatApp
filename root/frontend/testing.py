import flet as ft

def main(page: ft.Page):

	def create_cards():


		_dict = {
				'contact1': {
					'id': 123456,
					'name':'lorem psium'
				},
				'contact2': {
					'id': 7890,
					'name':'second name'
				}
		}

		items=[]

		for k, _dict in _dict.items():
			print(_dict)
			card = ft.ElevatedButton(
	                  content=ft.Container(
		                  data = _dict['id'],
		                  width=300,
		                  height=80,
		                  border_radius=ft.border_radius.all(
			                  15
		                  ),
		                  padding=ft.padding.all(0),
		                  content=ft.Row(
			                  alignment="start",
			                  spacing=5,
			                  controls=[
					                  ft.Icon(
						                  name=ft.icons.CHECK_CIRCLE_ROUNDED,
						                  color=ft.colors.GREEN_300,
						                  size=20,
					                  ),
				                  ft.Text(_dict['name'], size=20)
				                  ],
			                  )
		                  )
                    )
			print(card)
			items.append(card)
		print(type(items))
		return items

	c = ft.Column(
	          spacing=0, controls=create_cards()
	      )

	page.add(c)

ft.app(target=main)