import wx
import os
import re

class MainFrame(wx.Frame):
	filename = ''
	FRData = wx.FindReplaceData()
	attr = wx.TextAttr("black", "white")

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title = title, size = (640, 480))
		self.InitUI()

	def InitUI(self):
		menubar = wx.MenuBar()
#File Menu
		fileMenu = wx.Menu()
		newItem = wx.MenuItem(fileMenu, wx.ID_NEW, text = "New")
		fileMenu.AppendItem(newItem)
		openItem = wx.MenuItem(fileMenu, wx.ID_OPEN, text = "Open...")
		fileMenu.AppendItem(openItem)
		saveItem = wx.MenuItem(fileMenu, wx.ID_SAVE, text = "Save")
		fileMenu.AppendItem(saveItem)		
		fileMenu.AppendSeparator()
		quit = wx.MenuItem(fileMenu, wx.ID_EXIT, text = "Quit")
		fileMenu.AppendItem(quit)
		menubar.Append(fileMenu, '&File')
#Edit Menu
		editMenu = wx.Menu()
		copyItem = wx.MenuItem(editMenu, wx.ID_COPY, text = "Copy")
		editMenu.AppendItem(copyItem)
		cutItem = wx.MenuItem(editMenu, wx.ID_CUT, text = "Cut")
		editMenu.AppendItem(cutItem)
		pasteItem = wx.MenuItem(editMenu, wx.ID_PASTE, text = "Paste")
		editMenu.AppendItem(pasteItem)
		editMenu.AppendSeparator()
		findItem = wx.MenuItem(editMenu, wx.ID_FIND, text = "Find...")
		editMenu.AppendItem(findItem)
		replaceItem = wx.MenuItem(editMenu, wx.ID_REPLACE, text = "Replace...")
		editMenu.AppendItem(replaceItem)
		menubar.Append(editMenu, '&Edit')
#Settings Menu
		settMenu = wx.Menu()
		fontItem = wx.MenuItem(settMenu, 100, text = "Fonts")
		settMenu.AppendItem(fontItem)
		bgColourItem = wx.MenuItem(settMenu, 101, text = "Background Colours")
		settMenu.AppendItem(bgColourItem)
		txColourItem = wx.MenuItem(settMenu, 102, text = "Text Colours")
		settMenu.AppendItem(txColourItem)
		menubar.Append(settMenu, '&Settings')

		self.SetMenuBar(menubar)
		self.text = wx.TextCtrl(self, -1, style = wx.EXPAND|wx.TE_MULTILINE)
		self.text.SetDefaultStyle(self.attr)
		self.Bind(wx.EVT_MENU, self.menuHandler)
		self.Centre()
		self.Show(True)
		self.Bind(wx.EVT_FIND, self.onFind)
		#self.Bind(wx.EVT_FIND_REPLACE, self.onReplace)
		self.Bind(wx.EVT_FIND_REPLACE_ALL, self.onReplaceAll)

	def menuHandler(self, event):
		id = event.GetId()
		if id == wx.ID_NEW:
			self.text.Clear()

		elif id == wx.ID_OPEN:
			dialog = wx.FileDialog(self, "Open...", os.getcwd(), style=wx.FD_OPEN)
			if dialog.ShowModal() == wx.ID_OK:
				self.filename = dialog.GetPath()
				self.text.LoadFile(self.filename)
			self.SetTitle("Editor - %s"%self.filename)
			dialog.Destroy()

		elif id == wx.ID_SAVE:
			dialog = wx.FileDialog(self, "Save", os.getcwd(), style=wx.FD_SAVE)
			if dialog.ShowModal() == wx.ID_OK:
				self.filename = dialog.GetPath()
				self.text.SaveFile(self.filename)
			self.SetTitle("Editor - %s"%self.filename)
			dialog.Destroy()

		elif id == wx.ID_COPY:
			if self.text.CanCopy():
				self.text.Copy()

		elif id == wx.ID_CUT:
			if self.text.CanCut():
				self.text.Cut()

		elif id == wx.ID_PASTE:
			if self.text.CanPaste():
				self.text.Paste()

		elif id == wx.ID_FIND:
			find = wx.FindReplaceDialog(self, data = self.FRData, title = "Find", style = wx.FR_NOUPDOWN|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD)
			find.Show()

		elif id == wx.ID_REPLACE:
			rep = wx.FindReplaceDialog(self, data = self.FRData, title = "Replace", style = wx.FR_REPLACEDIALOG|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD)
			rep.Show()

		elif id == 100:
			font = wx.GetFontFromUser(self, caption = "Select Font")
			self.attr = wx.TextAttr(font = font)
			length = len(self.text.GetValue())
			self.text.SetStyle(0, length, self.attr)

		elif id == 101:
			colour = wx.GetColourFromUser(self, caption = "Background Colour")
			self.attr = wx.TextAttr(colBack = colour)
			length = len(self.text.GetValue())
			self.text.SetStyle(0, length, self.attr)

		elif id == 102:
			colour = wx.GetColourFromUser(self, caption = "Text Colour")
			self.attr = wx.TextAttr(colText = colour)
			length = len(self.text.GetValue())
			self.text.SetStyle(0, length, self.attr)

		elif id == wx.ID_EXIT:
			exit()

	def onFind(self, event):
		self.onHighLightClear()
		content = self.text.GetValue()
		findStr = self.FRData.GetFindString()
		size = len(findStr)
		for pos in range(0, len(content) - size):
			pos = content.find(findStr, pos)
			if pos == -1:
				return
			self.text.SetInsertionPoint(pos = pos)
			self.text.SetStyle(pos, pos + size, wx.TextAttr(colBack = "yellow"))

	def onHighLightClear(self):
		content = self.text.GetValue()
		self.text.SetStyle(0, len(content), self.attr)

	#def onReplace(self, event):
	#	self.onHighLightClear()
	#	pos = self.text.GetInsertionPoint()
	#	content = self.text.GetValue()
	#	findStr = self.FRData.GetFindString()
	#	repStr = self.FRData.GetReplaceString()
	#	size = len(findStr)
	#	for pos in range(pos, len(content) - size):
	#		pos = content.find(findStr, pos)
	#		if pos == -1:
	#			return
	#		left = content[0:pos]
	#		right = content[pos + size:]
	#		content = "%s%s%s"%(left, repStr, right)
	#		self.text.Clear()
	#		self.text.AppendText(content)

	def onReplaceAll(self, event):
		self.onHighLightClear()
		content = self.text.GetValue()
		findStr = self.FRData.GetFindString()
		repStr = self.FRData.GetReplaceString()
		size = len(findStr)
		for pos in range(0, len(content) - size):
			pos = content.find(findStr, pos)
			if pos == -1:
				return
			self.text.SetInsertionPoint(pos = pos)
			left = content[0:pos]
			right = content[pos + size:]
			content = "%s%s%s"%(left, repStr, right)
			self.text.Clear()
			self.text.AppendText(content)

if __name__ == "__main__":
	root = wx.App()
	MainFrame(None,'Editor')
	root.MainLoop()
