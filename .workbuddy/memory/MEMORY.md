# 长期记忆

## 技能：dashboard-generator 已预置配置（2026-04-03）

- **配置文件**：`C:\Users\bobo\.workbuddy\skills\codebuddy-skill-1775177246515\config.json`
- **数据库**：MySQL @ `mysql-zk-kang61753663-3ddd.a.aivencloud.com:16497`，库名 `test`，用户 `avnadmin`（Aiven云，需SSL）
- **GitHub Token**：已保存（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）
- **邮箱**：`15353124116@163.com`，SMTP 163，授权码已保存
- **下次使用**：用户只需提供表名，其余全部自动读取配置

---

## 项目：微信自动化发送消息

- **工作目录**：`c:\Users\bobo\WorkBuddy\Claw\`
- **主脚本**：`send_wechat3.py`
- **目标群聊**：天来三（常量 `TARGET_GROUP`）
- **发送消息**：我是AI（常量 `MESSAGE`）
- **依赖库**：`pyautogui`, `pyperclip`, `ctypes`, `pywinauto 0.6.9`
- **运行方式**：`python send_wechat3.py`（需要微信桌面端已登录）
- **关键修复记录**：
  - 2026-03-31：修复搜索后直接按 Enter 导致进入错误群聊的问题；改为 pywinauto UIA 遍历 + 坐标兜底双策略精确点击目标群聊条目
