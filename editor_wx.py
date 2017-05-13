import wx
import os

class MainFrame(wx.Frame):
	Filename = ''
	FRData = wx.FindReplaceData()
	TAttr = wx.TextAttr("black", "white")

	def __init__(self, parent):
		super(MainFrame, self).__init__(parent, title = "Editor - New", size = (640, 480))
		self.InitUI()

	def InitUI(self):
		menubar = wx.MenuBar()
#File Menu
		FileMenu = wx.Menu()
		newItem = wx.MenuItem(FileMenu, wx.ID_NEW, text = "New")
		FileMenu.AppendItem(newItem)
		openItem = wx.MenuItem(FileMenu, wx.ID_OPEN, text = "Open...")
		FileMenu.AppendItem(openItem)
		saveItem = wx.MenuItem(FileMenu, wx.ID_SAVE, text = "Save")
		FileMenu.AppendItem(saveItem)		
		FileMenu.AppendSeparator()
		quit = wx.MenuItem(FileMenu, wx.ID_EXIT, text = "Quit")
		FileMenu.AppendItem(quit)
		menubar.Append(FileMenu, '&File')
#Edit Menu
		EditMenu = wx.Menu()
		cutItem = wx.MenuItem(EditMenu, wx.ID_CUT, text = "Cut")
		EditMenu.AppendItem(cutItem)
		copyItem = wx.MenuItem(EditMenu, wx.ID_COPY, text = "Copy")
		EditMenu.AppendItem(copyItem)
		pasteItem = wx.MenuItem(EditMenu, wx.ID_PASTE, text = "Paste")
		EditMenu.AppendItem(pasteItem)
		EditMenu.AppendSeparator()
		findItem = wx.MenuItem(EditMenu, wx.ID_FIND, text = "Find...")
		EditMenu.AppendItem(findItem)
		replaceItem = wx.MenuItem(EditMenu, wx.ID_REPLACE, text = "Replace...")
		EditMenu.AppendItem(replaceItem)
		clearItem = wx.MenuItem(EditMenu, 103, text = "Clear Highlight")
		EditMenu.AppendItem(clearItem)
		menubar.Append(EditMenu, '&Edit')
#Settings Menu
		SettMenu = wx.Menu()
		fontItem = wx.MenuItem(SettMenu, 100, text = "Fonts")
		SettMenu.AppendItem(fontItem)
		txColourItem = wx.MenuItem(SettMenu, 101, text = "Text Colours")
		SettMenu.AppendItem(txColourItem)
		bgColourItem = wx.MenuItem(SettMenu, 102, text = "Background Colours")
		SettMenu.AppendItem(bgColourItem)
		menubar.Append(SettMenu, '&Settings')

		self.SetMenuBar(menubar)
		self.Text = wx.TextCtrl(self, -1, style = wx.EXPAND|wx.TE_MULTILINE|wx.TE_RICH2) #Inorder to set text attributes on windows, an 'wx.TE_RICH2' must be added
		self.Text.SetDefaultStyle(self.TAttr)
		self.Bind(wx.EVT_MENU, self.menuHandler)
		self.Show(True)
		self.Bind(wx.EVT_FIND, self.onFind)
		#self.Bind(wx.EVT_FIND_REPLACE, self.onReplace)
		self.Bind(wx.EVT_FIND_REPLACE_ALL, self.onReplaceAll)
		self.Bind(wx.EVT_TEXT, self.onModified)
		self.Bind(wx.EVT_CLOSE, self.onExit)

	def menuHandler(self, event):
		id = event.GetId()
		if id == wx.ID_NEW:
			self.Text.Clear()
			self.SetTitle("Editor - New")

		elif id == wx.ID_OPEN:
			dialog = wx.FileDialog(self, "Open...", os.getcwd(), style=wx.FD_OPEN)
			if dialog.ShowModal() == wx.ID_OK:
				self.Filename = dialog.GetPath()
				self.Text.LoadFile(self.Filename)
			self.SetTitle("Editor - %s"%self.Filename)
			dialog.Destroy()

		elif id == wx.ID_SAVE:
			dialog = wx.FileDialog(self, "Save", os.getcwd(), style=wx.FD_SAVE)
			if dialog.ShowModal() == wx.ID_OK:
				self.Filename = dialog.GetPath()
				self.Text.SaveFile(self.Filename)
			self.SetTitle("Editor - %s"%self.Filename)
			dialog.Destroy()

		elif id == wx.ID_COPY:
			if self.Text.CanCopy():
				self.Text.Copy()

		elif id == wx.ID_CUT:
			if self.Text.CanCut():
				self.Text.Cut()

		elif id == wx.ID_PASTE:
			if self.Text.CanPaste():
				self.Text.Paste()

		elif id == wx.ID_FIND:
			find = wx.FindReplaceDialog(self, data = self.FRData, title = "Find", style = wx.FR_NOUPDOWN|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD)
			find.Show()

		elif id == wx.ID_REPLACE:
			rep = wx.FindReplaceDialog(self, data = self.FRData, title = "Replace", style = wx.FR_REPLACEDIALOG|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD)
			rep.Show()

		elif id == 100: #Fonts
			font = wx.GetFontFromUser(self, caption = "Select Font")
			self.TAttr = wx.TextAttr(font = font)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)

		elif id == 101: #Text Colours
			colour = wx.GetColourFromUser(self, caption = "Text Colour")
			self.TAttr = wx.TextAttr(colText = colour)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)

		elif id == 102: #BG Colours
			colour = wx.GetColourFromUser(self, caption = "Background Colour")
			self.TAttr = wx.TextAttr(colBack = colour)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)


		elif id == 103:
			self.onHighLightClear()

		elif id == wx.ID_EXIT:
			self.onExit(wx.EVT_CLOSE)

	def onExit(self, event):
		if self.Text.IsModified():
			dialog = wx.MessageDialog(self, "File is modified! Save?", caption = "Alert", style = wx.YES_NO|wx.STAY_ON_TOP|wx.CENTRE|wx.CANCEL)
			status = dialog.ShowModal()
			if status == wx.ID_YES:
				saveDialog = wx.FileDialog(self, "Save", os.getcwd(), style=wx.FD_SAVE)
				if saveDialog.ShowModal() == wx.ID_OK:
					self.Filename = saveDialog.GetPath()
					self.Text.SaveFile(self.Filename)
					exit()
				else:
					saveDialog.Destroy()
					dialog.Destroy()
					return
			elif status == wx.ID_NO:
					dialog.Destroy()
					exit()
			else:
				dialog.Destroy()
				return
		else:
			exit()

	def onHighLightClear(self):
		content = self.Text.GetValue()
		self.Text.SetStyle(0, len(content), style = self.TAttr)
		self.Text.Clear()
		self.Text.AppendText(content)

	def onFind(self, event):
		self.onHighLightClear()
		content = self.Text.GetValue()
		findStr = self.FRData.GetFindString()
		size = len(findStr)
		for pos in range(0, len(content) - size):
			pos = content.find(findStr, pos)
			if pos == -1:
				return
			self.Text.SetInsertionPoint(pos = pos)
			self.Text.SetStyle(pos, pos + size, wx.TextAttr(colBack = "green"))

	#def onReplace(self, event):
	#	self.onHighLightClear()
	#	pos = self.Text.GetInsertionPoint()
	#	content = self.Text.GetValue()
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
	#		self.Text.Clear()
	#		self.Text.AppendText(content)

	def onReplaceAll(self, event):
		self.onHighLightClear()
		content = self.Text.GetValue()
		findStr = self.FRData.GetFindString()
		repStr = self.FRData.GetReplaceString()
		size = len(findStr)
		for pos in range(0, len(content) - size):
			pos = content.find(findStr, pos)
			if pos == -1:
				return
			self.Text.SetInsertionPoint(pos = pos)
			left = content[0:pos]
			right = content[pos + size:]
			content = "%s%s%s"%(left, repStr, right)
			self.Text.Clear()
			self.Text.AppendText(content)

	def onModified(self, event):
		title = self.GetTitle()
		if title[-1:] != '*':
			self.SetTitle("%s%s"%(title, '*'))

if __name__ == "__main__":
	root = wx.App()
	MainFrame(None)
	root.MainLoop()