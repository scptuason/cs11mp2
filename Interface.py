# Interface
# Ryan Marcel Ibay (2018-21278)
# Shawn Christian Tuason (2018-02438)
# Please type your names and student numbers!

import pyglet
import Engine

from pyglet.window import mouse
from pyglet.window import key


class Rectangle(object): # for the personalized rectangle
	def __init__(self, x1, y1, x2, y2, batch):
		self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
			('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),	# Coordinates for Rectangle Size
			('c4B', [248, 248, 242, 1] * 4)		# Rectangle Color
		)

class TextBox(object): # for the textbox
	def __init__(self, text, x, y, width, batch):
		self.document = pyglet.text.document.UnformattedDocument(text)
		self.document.set_style(0, len(self.document.text), 
			dict(color=(0, 0, 0, 255))
		)
		font = self.document.get_font()
		height = font.ascent - font.descent

		self.layout = pyglet.text.layout.IncrementalTextLayout(
			self.document, width, height, multiline=False, batch=batch)
		self.caret = pyglet.text.caret.Caret(self.layout)

		self.layout.x = x
		self.layout.y = y

		# Rectangular Outline
		pad = 2
		self.rectangle = Rectangle(x - pad, y - pad, 
								   x + width + pad, y + height + pad, batch)

	def hit_test(self, x, y):
		return (0 < x - self.layout.x < self.layout.width and
				0 < y - self.layout.y < self.layout.height)

class Window(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(600, 320, style=Window.WINDOW_STYLE_TOOL, caption='Cryptographer')

		self.batch = pyglet.graphics.Batch()
                # for the labels and instructions
		self.labels = [
			pyglet.text.Label('Cryptographer',font_name='Arial', font_size=22, italic=True, bold=True, x=20, y=275,
							  color=(255, 255, 255, 255), batch=self.batch),
			pyglet.text.Label("Instructions: 'Ctrl + Enter' to encrypt, 'Shift + Enter' to decrypt.", font_name='Arial', italic=True, x=20, y=240,
							  color=(255, 255, 255, 255), batch=self.batch),
			pyglet.text.Label("Input 'Message' or 'Cipher', accordingly, then 'Right-Ctrl' to save or load.", font_name='Arial', italic=True, x=20, y=220,
							  color=(255, 255, 255, 255), batch=self.batch),
			pyglet.text.Label("Ciphers: 'Substitution' and 'Caesar'.",font_name='Arial', italic=True, x=20, y=190,
							  color=(255, 255, 255, 255), batch=self.batch),
			pyglet.text.Label('Cipher Mode:', font_name='Arial', x=25, y=110, anchor_y='bottom',
							  color=(255, 255, 255, 255), batch=self.batch),
			pyglet.text.Label('Input Message:', font_name='Arial', x=25, y=70, 
							  anchor_y='bottom', color=(255, 255, 255, 255), 
							  batch=self.batch),
			pyglet.text.Label('Cipher Key:', font_name='Arial',  x=25, y=30, 
							  anchor_y='bottom', color=(255, 255, 255, 255), 
							  batch=self.batch),
			pyglet.text.Label('Save/Load?', font_name='Arial',  x=25, y=150, 
							  anchor_y='bottom', color=(255, 255, 255, 255), 
							  batch=self.batch)                                   
		]

		self.widgets = [
			TextBox('', 160, 110, self.width - 210, self.batch),
			TextBox('', 160, 70, self.width - 210, self.batch),
			TextBox('', 160, 30, self.width - 210, self.batch),
			TextBox('', 160, 150, self.width - 410, self.batch),
			TextBox('', 360, 150, self.width - 410, self.batch),
		]
		
		self.text_cursor = self.get_system_mouse_cursor('text')
		self.focus = None

	def on_resize(self, width, height):
		super(Window, self).on_resize(width, height)
		for widget in self.widgets:
			widget.width = width - 110

	def on_draw(self):
		pyglet.gl.glClearColor(0.1, 0.1, 0.1, 0.1)
		self.clear()
		self.batch.draw()

	def on_mouse_motion(self, x, y, dx, dy):
		for widget in self.widgets:
			if widget.hit_test(x, y):
				self.set_mouse_cursor(self.text_cursor)
				break
		else:
			self.set_mouse_cursor(None)

	def on_mouse_press(self, x, y, button, modifiers):
		for widget in self.widgets:
			if widget.hit_test(x, y):
				self.set_focus(widget)
				break
		else:
			self.set_focus(None)

		if self.focus:
			self.focus.caret.on_mouse_press(x, y, button, modifiers)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.focus:
			self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

	def on_text(self, text):
		if self.focus:
			self.focus.caret.on_text(text)

	def on_text_motion(self, motion):
		if self.focus:
			self.focus.caret.on_text_motion(motion)
	  
	def on_text_motion_select(self, motion):
		if self.focus:
			self.focus.caret.on_text_motion_select(motion)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.TAB:
			if modifiers & pyglet.window.key.MOD_SHIFT:
				dir = -1
			else:
				dir = 1
			if self.focus in self.widgets:
				i = self.widgets.index(self.focus)
			else:
				i = 0
				dir = 0
			self.set_focus(self.widgets[(i + dir) % len(self.widgets)])
		
		# For Translating, encrypting, decrypting files:
		elif symbol == pyglet.window.key.ENTER:
			if modifiers & pyglet.window.key.MOD_CTRL:
				# Encryption Process:
				mode = self.widgets[0].document.text
				message = self.widgets[1].document.text
				key = self.widgets[2].document.text

				if mode in 'Caesar c C caesar'.split():
					translated_message = Engine.CaesarE(mode, message, int(key))
				elif mode in 'Substitution substitution S s'.split():
					translated_message = Engine.SubstitutionCipherE(mode, message, key)
				else:
					translated_message = 'Invalid.'

				self.labels[0].document.text = str(translated_message)	# Replaces the header with the translation.

			elif modifiers & pyglet.window.key.MOD_SHIFT:
				# Decryption Process:
				mode = self.widgets[0].document.text
				message = self.widgets[1].document.text
				key = self.widgets[2].document.text

				if mode in 'Caesar c C caesar'.split():
					translated_message = Engine.CaesarD(mode, message, int(key))
				
				elif mode in 'Substitution substitution S s'.split():
					translated_message = Engine.SubstitutionCipherD(mode, message, key)

				else:
					translated_message = 'Invalid.'

				self.labels[0].document.text = translated_message	# Replaces the header with the translation.
			
			else:
				i = 0
				dir = 0

		# For opening and closing files:
		elif symbol == pyglet.window.key.RCTRL:
			directory_c = 'cipher.txt'
			directory_m = 'crypt.txt'

			mode = self.widgets[0].document.text
			message = self.widgets[1].document.text
			key = self.widgets[2].document.text
			saves = self.widgets[3].document.text
			loads = self.widgets[4].document.text

			if saves in 'Cipher cipher c'.split()  and len(key) > 0:
				Engine.SaveItem(self.widgets[2].document.text, directory_c)
				self.labels[0].document.text = 'Cipher Saved.'	# Replaces the header with the text.
			
			elif saves in 'Message message m'.split():
				if mode in 'Caesar c C caesar'.split():
					translated_message = Engine.CaesarE(mode, message, int(key))
					Engine.SaveItem(translated_message, directory_m)
					self.labels[0].document.text = 'Message Saved.' # Replaces the header with the text.
				elif mode in 'Substitution substitution S s'.split():
					translated_message = Engine.SubstitutionCipherE(mode, message, key)
					Engine.SaveItem(translated_message, directory_m)
					self.labels[0].document.text = 'Message Saved.' # Replaces the header with the text.
				else:
					self.labels[0].document.text = 'Save Failed.' # Replaces the header with the text.
			
			elif loads in 'Cipher cipher c':		
				self.labels[0].document.text = Engine.OpenItem(directory_c)
			
			elif loads in 'Message message m':
				self.labels[0].document.text = Engine.OpenItem(directory_m)
			else:
				self.labels[0].document.text = 'Load Failed.'

		elif symbol == pyglet.window.key.ESCAPE:
			pyglet.app.exit()
		
		else:
			i = 0
			dir = 0

	def set_focus(self, focus):
		if self.focus:
			self.focus.caret.visible = False
			self.focus.caret.mark = self.focus.caret.position = 0

		self.focus = focus
		if self.focus:
			self.focus.caret.visible = True
			self.focus.caret.mark = 0
			self.focus.caret.position = len(self.focus.document.text)

window = Window(resizable=True)
pyglet.app.run()
