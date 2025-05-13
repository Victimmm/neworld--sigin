 


  
# 新界梯子每日自动签到工具

## 脚本介绍 
此脚本为 **Neworld** 新界梯子的每日自动签到工具。部署好工作流后，您可以每天定时签到，增加梯子的使用时间和流量。

## 使用方式

### 1. 项目标星与 Fork
首先，您需要将该项目 **星标** 并 **Fork** 到自己的仓库。  
![image](https://github.com/user-attachments/assets/5bfeebe4-5e9e-4ca7-b306-b5a8e16f8b7f)

### 2. 配置账号和密码
在您的仓库中，进入 **Settings** 页面，找到 **Secrets** 部分，配置您的账号和密码。  
添加两个属性：
- `USERNAME`：新界的账号
- `PASSWORD`：新界的密码

![image](https://github.com/user-attachments/assets/616a5435-684e-4eba-9b15-a6a4a4300b05)

### 3. 手动触发工作流
进入 **Actions** 页面，找到 **Python application** 工作流，手动触发一次，以测试工作流是否正常工作。  
![image](https://github.com/user-attachments/assets/fa5921ff-f52f-48a8-923c-4a4a61ec12d6)

### 4. 查看工作流执行日志
点击查看工作流的执行日志，确认签到是否成功。  
![image](https://github.com/user-attachments/assets/7835039b-a68b-46ae-95a8-75fb5c367bd6)

### 5. 验证签到成功
查看 `response` 中的内容，若 Unicode 编码转义后的中文提示为 "签到成功"，则表示工作流部署成功。

---

