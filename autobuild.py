
# coding=UTF-8
# __author__ = '照顾一下'

import Tkinter
import Tkconstants
import tkFileDialog
import sendmsg
import xcodebuild


class XcodeAutoBuildDialog(Tkinter.Frame):

    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        self.archive_dir = ""

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 15, 'pady': 15}

        # define buttons
        button1 = Tkinter.Button(self, text='选择xcode项目所在文件夹', command=self.open_xcode_filename)
        button1.pack(**button_opt)

        button2 = Tkinter.Button(self, text='选择打包输出文件夹', command=self.open_archive_filename)
        button2.pack(**button_opt)

        button3 = Tkinter.Button(self, text='清空打包输出文件夹', command=self.delete_old_ipa_file)
        button3.pack(**button_opt)

        button4 = Tkinter.Button(self, text='一键打包上传', command=self.build)
        button4.pack(**button_opt)

    # 获取项目所在文件夹
    def open_xcode_filename(self):

        filename = tkFileDialog.askdirectory()
        xcode.fix_project_params(filename)

    # 获取打包输出文件夹
    def open_archive_filename(self):

        self.archive_dir = tkFileDialog.askdirectory()
        xcode.fix_archive_params(self.archive_dir)

    # 删除原来的IPA文件
    def delete_old_ipa_file(self):
        xcode.delete_old_ipa()

    # 打包
    def build(self):
        path = xcode.auto_build()
        suc = sendmsg.send_ipa(path)
        if suc == 1:
            sendmsg.send_qq_email("哈哈", "打包成功了，快去更新吧，更新地址http://fir.zhaoguyixia.club/274e")
        else:
            sendmsg.send_qq_email("哎", "上传失败，快看看什么问题吧")

if __name__ == '__main__':

    xcode = xcodebuild.XcodeBuild()
    root = Tkinter.Tk()
    XcodeAutoBuildDialog(root).pack()
    root.mainloop()



