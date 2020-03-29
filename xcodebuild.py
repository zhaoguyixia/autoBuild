
# coding=UTF-8
# __author__='照顾一下'

import os
import subprocess
import tkMessageBox
import re


class XcodeBuild():

    def __init__(self):
        self.project_dir = ""
        self.archive_dir = ""
        self.project_type = ""
        self.project_name = ""
        self.archive_type = "Release"  # Debug or Release
        self.scheme_name = ""
        self.archivePath = ""

    def fix_project_params(self, project_file_dir):

        print project_file_dir

        if project_file_dir == "":
            tkMessageBox.showerror("警告", "请选择项目所在文件夹")
            return
        # 判断是否存在xcworkspace的文件
        files = os.listdir(project_file_dir)
        print files
        if files.count == 0:
            tkMessageBox.showerror("警告", "你选择的是空文件夹")
            return
        for filename in files:
            if filename.find("xcworkspace") > 0:
                # 是用了pod管理
                self.project_type = '-workspace'
                self.project_name = filename
                self.project_dir = project_file_dir
                self.set_project_name(filename)
                return
            elif filename.find("xcodeproj") > 0:
                self.project_type = '-project'
                self.project_name = filename
                self.project_dir = project_file_dir
                self.set_project_name(filename)
                return
        tkMessageBox.showerror("警告", "你选择的不是xcode项目")

    def set_project_name(self, filename):
        if filename == "":
            return
        name_arr = re.split('\.|/', filename)
        self.scheme_name = name_arr[0]
        print "项目名  "+self.scheme_name

    def fix_archive_params(self, archive_file_dir):
        print archive_file_dir
        if archive_file_dir == "":
            tkMessageBox.showerror("警告", "请选择导出文件夹")
            return
        self.archive_dir = archive_file_dir

    def delete_old_ipa(self):
        print "---------------"+self.archive_dir
        if self.archive_dir == "" or self.archive_dir.find("build") <= 0:
            print "选择的文件夹不对"
            tkMessageBox.showinfo("警告", "选择的文件夹不对")
            return
        if self.archive_dir.find("hope-iOS") >= 0:
            tkMessageBox.showinfo("警告", "这可是项目文件夹，不能删的啊")
            return
        files = os.listdir(self.archive_dir)
        print files
        if files.count == 0:
            return
        for filename in files:
            if filename == "ExportOptions.plist" or filename == ".DS_Store":
                continue
            else:
                absolute_path = self.archive_dir+"/"+filename
                if os.path.exists(absolute_path) == 1:
                    try:
                        if os.path.isdir(absolute_path) == 1:
                            subprocess.call(["rm", "-rf", absolute_path])
                        else:
                            subprocess.call(["rm", "-f", absolute_path])
                        print "删除  " + absolute_path + " 成功"
                    except subprocess.CalledProcessError, err:
                        print "删除失败"+err

    def check_params(self):
        if self.project_dir == "":
            tkMessageBox.showerror("警告", "没有选择项目")
            return False
        if self.archive_dir == "":
            tkMessageBox.showerror("警告", "没有选择导出路径")
            return False
        if self.scheme_name == "":
            tkMessageBox.showerror("警告", "你选择的不是xcode项目")
            return False

        if os.path.exists(self.archive_dir+"/ExportOptions.plist") == 0:
            tkMessageBox.showerror("警告", "ExportOptions.plist文件不存在，请使用xcode手动生成一次，注意，thining选none，勾去掉")
            return False
        return True

    def auto_build(self):

        if self.check_params() == 0:
            return

        print "-------------自动化打包-----------"

        self.archivePath = self.archive_dir+"/"+self.scheme_name

        os.chdir(self.project_dir)

        print os.getcwd()

        subprocess.call(['xcodebuild', 'archive', self.project_type, self.project_name,
                         '-configuration', self.archive_type,
                         '-scheme', self.scheme_name,
                         '-archivePath', self.archivePath])

        print "打包完成之后需要进入到包所在文件夹位置"

        os.chdir(self.archive_dir)

        archive_file = self.scheme_name+".xcarchive"

        print "-------------生成ipa-----------"
        subprocess.call(['xcodebuild', '-exportArchive',
                         '-archivePath', archive_file,
                         '-exportPath', './',
                         '-exportOptionsPlist', 'ExportOptions.plist'])
        print("process complete")
        return self.archivePath+".ipa"
