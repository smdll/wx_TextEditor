# -*- coding: utf-8 -*-
import wx
import os

class MainFrame(wx.Frame):
	Filename = ''
	FRData = wx.FindReplaceData()
	TAttr = wx.TextAttr()
	lastPos = 0

	def __init__(self, parent):
		super(MainFrame, self).__init__(parent, title = u"记事本 - 新文件", size = (640, 480))
		self.InitUI()

	def InitUI(self):
		menubar = wx.MenuBar()
#文件菜单
		FileMenu = wx.Menu()
		newItem = wx.MenuItem(FileMenu, wx.ID_NEW, text = u"新建")
		FileMenu.AppendItem(newItem)
		openItem = wx.MenuItem(FileMenu, wx.ID_OPEN, text = u"打开...")
		FileMenu.AppendItem(openItem)
		saveItem = wx.MenuItem(FileMenu, wx.ID_SAVE, text = u"保存")
		FileMenu.AppendItem(saveItem)		
		FileMenu.AppendSeparator()
		quit = wx.MenuItem(FileMenu, wx.ID_EXIT, text = u"退出")
		FileMenu.AppendItem(quit)
		menubar.Append(FileMenu, u'&文件')
#编辑菜单
		EditMenu = wx.Menu()
		undoItem = wx.MenuItem(EditMenu, wx.ID_UNDO, text = u"撤销")
		EditMenu.AppendItem(undoItem)
		redoItem = wx.MenuItem(EditMenu, wx.ID_REDO, text = u"重做")
		EditMenu.AppendItem(redoItem)
		EditMenu.AppendSeparator()
		cutItem = wx.MenuItem(EditMenu, wx.ID_CUT, text = u"剪切")
		EditMenu.AppendItem(cutItem)
		copyItem = wx.MenuItem(EditMenu, wx.ID_COPY, text = u"复制")
		EditMenu.AppendItem(copyItem)
		pasteItem = wx.MenuItem(EditMenu, wx.ID_PASTE, text = u"粘贴")
		EditMenu.AppendItem(pasteItem)
		EditMenu.AppendSeparator()
		replaceItem = wx.MenuItem(EditMenu, wx.ID_REPLACE, text = u"查找&&替换...")
		EditMenu.AppendItem(replaceItem)
		clearItem = wx.MenuItem(EditMenu, 103, text = u"清除高亮")
		EditMenu.AppendItem(clearItem)
		menubar.Append(EditMenu, u'&编辑')
#设置菜单
		SettMenu = wx.Menu()
		fontItem = wx.MenuItem(SettMenu, 100, text = u"字体")
		SettMenu.AppendItem(fontItem)
		txColourItem = wx.MenuItem(SettMenu, 101, text = u"文字颜色")
		SettMenu.AppendItem(txColourItem)
		bgColourItem = wx.MenuItem(SettMenu, 102, text = u"背景颜色")
		SettMenu.AppendItem(bgColourItem)
		menubar.Append(SettMenu, u'&设置')
#帮助菜单
		HelpMenu = wx.Menu()
		aboutItem = wx.MenuItem(HelpMenu, wx.ID_ABOUT, text = u"关于...")
		HelpMenu.AppendItem(aboutItem)
		menubar.Append(HelpMenu, u'&帮助')

		self.SetMenuBar(menubar)
		self.Text = wx.TextCtrl(self, -1, style = wx.EXPAND|wx.TE_MULTILINE|wx.TE_RICH2) #在Windows上必须加上'wx.TE_RICH2'才能正常显示字体颜色等文字属性
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
			self.SetTitle(u"记事本 - 新文件")
			self.Text.DiscardEdits()

		elif id == wx.ID_OPEN:
			dialog = wx.FileDialog(self, u"打开...", os.getcwd(), style=wx.FD_OPEN)
			if dialog.ShowModal() == wx.ID_OK:
				self.Filename = dialog.GetPath()
				self.Text.LoadFile(self.Filename)
				self.SetTitle(u"记事本 - %s"%self.Filename)
				self.Text.DiscardEdits()
			dialog.Destroy()

		elif id == wx.ID_SAVE:
			if self.Filename == '' or self.Text.IsModified():
				dialog = wx.FileDialog(self, u"保存", os.getcwd(), style=wx.FD_SAVE)
				if dialog.ShowModal() == wx.ID_OK:
					self.Filename = dialog.GetPath()
					self.Text.SaveFile(self.Filename)
					self.SetTitle(u"记事本 - %s"%self.Filename)
					self.Text.DiscardEdits()
				dialog.Destroy()
			else:
				self.Text.SaveFile(self.Filename)
				self.SetTitle(u"记事本 - %s"%self.Filename)
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

		elif id == wx.ID_REPLACE:
			rep = wx.FindReplaceDialog(self, data = self.FRData, title = u"查找&替换", style = wx.FR_REPLACEDIALOG|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD)
			rep.Show()

		elif id == 100: #字体
			font = wx.GetFontFromUser(self, caption = u"选择字体")
			self.TAttr = wx.TextAttr(font = font)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)

		elif id == 101: #文字颜色
			colour = wx.GetColourFromUser(self, caption = u"选择文字颜色")
			self.TAttr = wx.TextAttr(colText = colour)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)

		elif id == 102: #背景颜色
			colour = wx.GetColourFromUser(self, caption = u"选择背景颜色")
			self.TAttr = wx.TextAttr(colBack = colour)
			length = len(self.Text.GetValue())
			self.Text.SetStyle(0, length, self.TAttr)

		elif id == 103:
			self.onHighLightClear()

		elif id == wx.ID_ABOUT:
			wx.MessageBox(u"由SMD设计，一个记事本模拟器", u"关于", wx.OK, self)

		elif id == wx.ID_EXIT:
			self.onExit(wx.EVT_CLOSE)

	def onExit(self, event):
		if self.Text.IsModified():
			dialog = wx.MessageDialog(self, u"文件已修改！保存？", caption = u"提示", style = wx.YES_NO|wx.STAY_ON_TOP|wx.CENTRE|wx.CANCEL)
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
			wx.MessageBox(u"找不到'%s'"%findStr, u"提示", wx.OK, self)
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
			wx.MessageBox(u"找不到'%s'"%findStr, u"提示", wx.OK, self)
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
				wx.MessageBox(u"找不到'%s'"%findStr, u"提示", wx.OK, self)
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