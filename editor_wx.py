import wx
import os

class MainFrame(wx.Frame):
	Filename = ''
	FRData = wx.FindReplaceData()
	TAttr = wx.TextAttr()
	lastPos = 0

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
		undoItem = wx.MenuItem(EditMenu, wx.ID_UNDO, text = "Undo")
		EditMenu.AppendItem(undoItem)
		redoItem = wx.MenuItem(EditMenu, wx.ID_REDO, text = "Redo")
		EditMenu.AppendItem(redoItem)
		EditMenu.AppendSeparator()
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
#Help Menu
		HelpMenu = wx.Menu()
		aboutItem = wx.MenuItem(HelpMenu, wx.ID_ABOUT, text = "About...")
		HelpMenu.AppendItem(aboutItem)
		menubar.Append(HelpMenu, '&Help')

		self.SetMenuBar(menubar)
		self.Text = wx.TextCtrl(self, -1, style = wx.EXPAND|wx.TE_MULTILINE|wx.TE_RICH2) #Inorder to set text attributes on windows, an 'wx.TE_RICH2' must be added
		self.Text.SetDefaultStyle(self.TAttr)
		self.Text.DiscardEdits()
		self.Bind(wx.EVT_MENU, self.menuHandler)
		self.Show(True)
		self.Bind(wx.EVT_FIND, self.onFind)
		self.Bind(wx.EVT_FIND_NEXT, self.onFind)
		self.Bind(wx.EVT_FIND_REPLACE, self.onReplace)
		self.Bind(wx.EVT_FIND_REPLACE_ALL, self.onReplaceAll)
		self.Bind(wx.EVT_TEXT, self.onModified)
		self.Bind(wx.EVT_CLOSE, self.onExit)

	def menuHandler(self, event):
		id = event.GetId()
		if id == wx.ID_NEW:
			self.Text.Clear()
			self.SetTitle("Editor - New")
			self.Text.DiscardEdits()

		elif id == wx.ID_OPEN:
			dialog = wx.FileDialog(self, "Open...", os.getcwd(), style=wx.FD_OPEN)
			if dialog.ShowModal() == wx.ID_OK:
				self.Filename = dialog.GetPath()
				self.Text.LoadFile(self.Filename)
				self.SetTitle("Editor - %s"%self.Filename)
				self.Text.DiscardEdits()
			dialog.Destroy()

		elif id == wx.ID_SAVE:
			if self.Filename == '' or self.Text.IsModified():
				dialog = wx.FileDialog(self, "Save", os.getcwd(), style=wx.FD_SAVE)
				if dialog.ShowModal() == wx.ID_OK:
					self.Filename = dialog.GetPath()
					self.Text.SaveFile(self.Filename)
					self.SetTitle("Editor - %s"%self.Filename)
					self.Text.DiscardEdits()
				dialog.Destroy()
			else:
				self.Text.SaveFile(self.Filename)
				self.SetTitle("Editor - %s"%self.Filename)
				self.Text.DiscardEdits()

		elif id == wx.ID_UNDO:
			if self.Text.CanUndo():
				self.Text.Undo()

		elif id == wx.ID_REDO:
			if self.Text.CanRedo():
				self.Text.Redo()

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

		elif id == wx.ID_ABOUT:
			wx.MessageBox("Designed by SMD, a NotePad emulator.", "About", wx.OK, self)

		elif id == wx.ID_EXIT:
			self.onExit(wx.EVT_CLOSE)

	def onExit(self, event):
		if self.Text.IsModified():
			dialog = wx.MessageDialog(self, "File is modified! Save?", caption = "Alert", style = wx.YES_NO|wx.STAY_ON_TOP|wx.CENTRE|wx.CANCEL)
			status = dialog.ShowModal()
			if status == wx.ID_YES:
				self.onSave()
				exit()
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
				pos = 0
				break
			self.Text.SetStyle(pos, pos + size, wx.TextAttr(colBack = "green"))
		self.lastPos = content.find(findStr, self.lastPos + size)
		if self.lastPos == -1:
			self.lastPos = 0
			return
		self.Text.SetInsertionPoint(pos = self.lastPos)

	def onReplace(self, event):
		content = self.Text.GetValue()
		findStr = self.FRData.GetFindString()
		repStr = self.FRData.GetReplaceString()
		size = len(findStr)
		self.lastPos = content.find(findStr, self.lastPos)
		if self.lastPos == -1:
			self.lastPos = 0
			wx.MessageBox("String Not Found", "Alert", wx.OK, self)
			return
		left = content[0:self.lastPos]
		right = content[self.lastPos + size:]
		content = "%s%s%s"%(left, repStr, right)
		self.Text.Clear()
		self.Text.AppendText(content)

	def onReplaceAll(self, event):
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