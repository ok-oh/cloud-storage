# 环境配置
```
pip install esdk-obs-python
```

# 已有接口

* POST：/upload/<username>
  * 使用username身份上传文件
    * 为当前所上传文件的权限添加username的访问许可
  
* GET： /download/<filename>/<username>
  * 使用username身份下载文件
    * 有权限则成功下载
    * 无权限则无法下载
  
* GET： /list/<username>
  * 以username身份获取云盘中的文件列表
  
* DELETE：/delete/<filename>/<username>
  * 以username身份删除指定新闻
  
* POST：/addNewUser/<username>/<password>

  * 注册新的用户

* GET：/login/<username>/<password>

  * 检测用户登录是否通过
    * 成功返回“login pass"
    * 失败返回"permission denied"
  
* POST：/addPermission/<operator>/<targetFile>/<targetUser>
  
  * 以用户名为operator的身份为targetFile添加targetUser的可访问权限
  
    * 前提是operator对targetFile有权限
  
* DELETE：/deletePermission/<operator>/<targetFile>/<targetUser>
  
  * 以用户名为operator的身份为targetFile删除targetUser的可访问权限
    * 前提是operator对targetFile有权限
  
* GET：/getLog/<username>
  * 返回用户username的网盘文件变动日志
    * 是一个String数组


  

  

  

