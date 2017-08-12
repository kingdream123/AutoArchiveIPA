#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 项目需在Xcode 中 关闭 Automatically manage signing
# 描述文件UUID 查看, 终端 security cms -D -i XXX.mobileprovision; 倒数第二UUID字段
# RubyGems 镜像地址:https://gems.ruby-china.org/

# 上传fir 需要安装fir-cli: https://github.com/FIRHQ/fir-cli/blob/master/doc/install.md
# fir 的用户 api
fir_api_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 项目根目录
project_path = "/Users/remair/Temp/heixiu/heixiu"
# 打包后ipa存储目录
targerIPA_parth = "/Users/remair/Desktop/IPA"
# 编译模式 Debug Release
CONFIGURATION = "Release"

# 项目名称
project_name = "live"
scheme_name = "live"
# 工程类型 pod工程 -workspace 普通工程 -project
project_type = "-workspace"


# 证书名
AdHoc_CODE_SIGN_IDENTITY = "iPhone Developer: Qi Hao (AUQQ86799J)"
# 描述文件UUID
AdHoc_PROVISIONING_PROFILE = "f57371f4-4d19-4bb7-a2fc-b07ea2c27a16"

# 证书名
Enterprise_CODE_SIGN_IDENTITY = "2_iPhone Distribution:"
# 描述文件UUID
Enterprise_PROVISIONING_PROFILE = "2_f9da7ca4-79ae-4d07-90ee-b868b09bf7f1"

# 证书名
AppStore_CODE_SIGN_IDENTITY = "iPhone Distribution: Qi Hao (UNB7SGHL8H)"
# 描述文件UUID
AppStore_PROVISIONING_PROFILE = "396ef021-b66b-4e5f-8001-1f97217feefe"

# 证书名
Development_CODE_SIGN_IDENTITY = "iPhone Developer: Qi Hao (AUQQ86799J)"
# 描述文件UUID
Development_PROVISIONING_PROFILE = "f57371f4-4d19-4bb7-a2fc-b07ea2c27a16"


# 打包类型 1. Ad_hoc, 2. Enterprise, 3. AppStore, 4. Development
archive_type_dic = {"1":"Ad_hoc", "2":"Enterprise", "3":"AppStore", "4":"Development"}
# 导出ipa 所需要的plist
export_options_plist_dic = {"1":"AdHocExportOptionsPlist.plist", "2":"EnterpriseExportOptionsPlist.plist", "3":"AppStoreExportOptionsPlist.plist", "4":"DevelopmentExportOptionsPlist.plist"}


# ========================================== #
# ========================================== #
# 打包信息
def archive_info():
	print ("打包项目: %s\nScheme: %s" % (project_name, scheme_name))
	if project_type == "-workspace":
		tip_project_type = "Pod工程"
	else:
		tip_project_type = "普通工程"
	print ("工程类型: %s" % tip_project_type)
	print ("编译模式: %s" % CONFIGURATION)

# 打包方式选择
def parameter_input():

	global CODE_SIGN_IDENTITY			# 打包使用的 证书名
	global PROVISIONING_PROFILE			# 打包使用的 描述文件UUID
	global export_options_plist_file	# ipa 导出配置文件
	global archive_type

	print ("=======================")
	print ("===  请选择打包方式 ===")
	print ("=======================")
	print ("=    1. AdHoc	      =")
	print ("=    2. Enterprise    =")
	print ("=    3. AppStore      =")
	print ("=    4. Development   =")
	print ("=======================")
	archive_type = raw_input('请选择:')
	if archive_type.isdigit(): #判断输入的是纯数字
		if archive_type == "1":
			CODE_SIGN_IDENTITY = AdHoc_CODE_SIGN_IDENTITY
			PROVISIONING_PROFILE = AdHoc_PROVISIONING_PROFILE
		elif archive_type == "2":
			CODE_SIGN_IDENTITY = Enterprise_CODE_SIGN_IDENTITY
			PROVISIONING_PROFILE = Enterprise_PROVISIONING_PROFILE
		elif archive_type == "3":
			CODE_SIGN_IDENTITY = AppStore_CODE_SIGN_IDENTITY
			PROVISIONING_PROFILE = AppStore_PROVISIONING_PROFILE
		elif archive_type == "4":
			CODE_SIGN_IDENTITY = Development_CODE_SIGN_IDENTITY
			PROVISIONING_PROFILE = Development_PROVISIONING_PROFILE
		else:
			print ("输入错误请重新输入 (输入1~4数字即可)")
			return parameter_input()

		export_options_plist_file = export_options_plist_dic[archive_type]
		print ("选择的打包方式为: %s" % archive_type_dic[archive_type])
		print ("使用的证书: %s" % CODE_SIGN_IDENTITY)
		print ("使用的描述文件: %s" % PROVISIONING_PROFILE)
		print ("使用的ipa导出配置文件: %s" % export_options_plist_file)
	else:
		print ("输入错误请重新输入 (输入1~4数字即可)")
		return parameter_input()

# 清理项目 创建build目录
def clean_project_mkdir_build():
	print ("clean build ...")
	os.system('cd %s;xcodebui/ld clean' % project_path) # clean 项目

# archive项目
def build_project():
	print ("build %s %s start" % (scheme_name, CONFIGURATION))
	if project_type == "-workspace":
		project_suffix_name = "xcworkspace"
	else:
		project_suffix_name = "xcodeproj"

	global ipa_filename
	ipa_filename = time.strftime('_%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
	ipa_filename = scheme_name + "_" + archive_type_dic[archive_type] + ipa_filename
	os.system ('cd %s;xcodebuild archive %s %s.%s -scheme %s -configuration %s -archivePath %s/%s/build/%s CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" || exit' % (project_path, project_type, project_name, project_suffix_name, scheme_name, CONFIGURATION, targerIPA_parth, ipa_filename, project_name, CODE_SIGN_IDENTITY, PROVISIONING_PROFILE))

# 导出ipa 并输出到设置的存错目录
def build_ipa():
	xcodebuild_safe_path = "%s/xcodebuild-safe.sh" % os.getcwd() # 获取当前目录路径
	export_options_plist_path = "%s/%s" % (os.getcwd(), export_options_plist_dic[archive_type])
	os.system ('%s -exportArchive -archivePath %s/%s/build/%s.xcarchive -exportPath %s/%s -exportOptionsPlist %s' % (xcodebuild_safe_path, targerIPA_parth, ipa_filename, project_name, targerIPA_parth, ipa_filename, export_options_plist_path))

# # 上传fir
def upload_fir():
	global upload_fir_state

	if archive_type == "3": # AppStore 版本不上传fir
		upload_fir_state = True
		return

	if os.path.exists("%s/%s" % (targerIPA_parth, ipa_filename)):
		print ("上传fir ...")
		ret = os.system("fir publish '%s/%s/%s.ipa' --token='%s'" % (targerIPA_parth, ipa_filename, project_name, fir_api_token))
		print ("上传fir成功")
		upload_fir_state = ret
	else:
		upload_fir_state = False
		print("上传fir失败, 没有找到ipa文件")

# 输出包信息
def ipa_info():
	if upload_fir_state != False:
		print '\n'
		print "ipa路径: %s/%s/%s.ipa" % (targerIPA_parth, ipa_filename, project_name)
		print '\n'
		print ("打包完毕")


def main():
	# 打包信息
	archive_info()
	# 打包方式选择
	parameter_input()
	# # 清理项目 创建build目录
	clean_project_mkdir_build()
	# 编译项目
	build_project()
	# 导出ipa 并输出到设置的存错目录
	build_ipa()
	# 上传fir
	upload_fir()
	# 输出包信息
	ipa_info()

# 执行
main()







