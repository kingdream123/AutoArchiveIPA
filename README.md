# 自动打包脚本说明
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/kingdream123/AutoArchiveIPA/blob/master/LICENSE)&nbsp;
### 执行前准备:
---
#### 1. Xcode项目配置:
1.1 去掉 `Automatically manage signig`

![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/1.png)

1.2 选择相应的描述文件 
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/2.png)

---
#### 2. 环境配置:
2.1 上传fir 需要安装`fir-cli`, [fir-cli帮助](https://github.com/FIRHQ/fir-cli/blob/master/doc/install.md);

若无法安装请检查Ruby 镜像地址是否已更改为:`https://gems.ruby-china.org/` 

查看当前Ruby地址:

![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/4.png)

2.2 复制fir 用户api token, 赋值 `fir_api_token` 变量 
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/3.png)

---
#### 3. Python代码里面需修改的内容:
3.1 修改固定变量:
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/5.png)
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/6.png)

3.2 证书名称的获取: 打开 [钥匙串访问] 程序, 选择相应的`证书` -> 右击 -> `显示简介` -> 复制 `常用名称`
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/7.png) 
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/8.png)

3.3 描述文件UUID的查看: 

终端执行 `security cms -D -i XXX.mobileprovision`; 
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/9.png)
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/10.png)

---
#### 4. 执行Python脚本
如图 运行`AutoArchiveIPA.py`脚本
![](https://github.com/kingdream123/AutoArchiveIPA/blob/master/AutoArchiveIPA/pic/11.png)

若无法执行, 修改此文件权限为可执行 `$sudo chmod +x AutoArchiveIPA.py`
或者 直接修改为`777`权限:`$sudo chmod -R 777 AutoArchiveIPA.py`
然后再执行脚本

---
#### 5. 其他
5.1 关于xcodebuild-safe.sh脚本:[查看](https://stackoverflow.com/questions/33041109/xcodebuild-no-applicable-devices-found-when-exporting-archive)

5.2 关于exportOptionsPlist文件:[exportOptionsPlist文件](https://developer.apple.com/library/content/technotes/tn2339/_index.html)

根据xcodebuild -help提供的可选key可以知道，
compileBitcode、
embedOnDemandResourcesAssetPacksInBundle、
iCloudContainerEnvironment、
manifest、
onDemandResourcesAssetPacksBaseURL、
thinning这几个key用于非App Store导出的；
uploadBitcode、
uploadSymbols用于App Store导出；
method、teamID共用。

method的可选值为:
app-store, package, ad-hoc, enterprise, development, and developer-id

5.3 [xcodebuild](https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/xcodebuild.1.html)



