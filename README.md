# VCB-Studio-Update

获取 VCB 更新消息，将新文章发送至邮箱。

![1712157336501](image/README/1712157336501.png)

**本项目仅限个人使用，严禁用于违法用途！**

# linux 服务器部署方法

1. 下载仓库代码

   ```
   git clone https://github.com/LinXu-LinXu/VCB-Studio-Update.git
   ```
2. 下载 python 依赖库

   ```
   pip install requests bs4 smtplib
   ```
3. **修改 VCB_Update.py 文件中的邮箱信息**

   ```
   # 设置发件人和收件人的电子邮件地址
   FROM_EMAIL = "xxxxxxxxxxx@xxx.com"    # 发信人
   FROM_NAME = "Miku"
   FROM_PASSWORD = "xxxxxxxxxxxx"        # SMTP 邮箱密码
   TO_EMAIL = "xxxxxxxxxx@xxx.com"       # 收信人
   ```
4. 编写 shell 脚本

   创建 vcb_update.sh 文件，填入以下内容并**修改第一行内容为 VCB_Update.py 文件存放路径**

   ```
   cd /root/VCB
   python3 VCB_Update.py
   ```
   在后面运行时可能会碰到日志报错：Permission Denied

   可以使用 `chmod` 命令给脚本添加执行权限：`chmod +x /root/VCB/vcb_update.sh`
5. 设置定时任务

   使用命令 `crontab -e` 添加一个新 cron 作业

   在打开的文件中填入

   ```
   */20 * * * *  /root/VCB/vcb_update.sh > /tmp/load.log 2>&1
   ```
   其中第一段定时执行的频次，这里是每 20 分钟执行一次，具体规则与测试见 [这个网站](https://tool.lu/crontab/)

   第二段是第 4 步 shell 脚本的存放位置，第三段是打印日志。

   完成后退出保存
6. 至此部署完成，windows 端部署可以参考 [这篇文章](https://blog.csdn.net/m0_46629123/article/details/120070320) 解决。
