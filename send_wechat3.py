import time
import ctypes
import ctypes.wintypes
import pyperclip
import pyautogui
from PIL import Image

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

user32 = ctypes.windll.user32

TARGET_GROUP = "天来三"
MESSAGE      = "我是AI"

SEARCH_WAIT  = 3.0   # 等待搜索结果刷新的秒数
# 微信搜索结果列表布局（根据实际截图校准）
PANEL_WIDTH  = 250   # 左侧列表面板宽度（像素）
LIST_TOP     = 120   # 列表第一条结果距窗口顶部的偏移（像素）
ITEM_HEIGHT  = 64    # 每个搜索结果条目的高度（像素）


def get_win_rect(hwnd):
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top


def capture_search_panel(hwnd, filename="debug_panel.png"):
    """截取微信左侧搜索结果面板区域，保存为 filename"""
    wx, wy, ww, wh = get_win_rect(hwnd)
    panel_w = min(PANEL_WIDTH, ww // 3)
    region = (wx, wy + LIST_TOP, panel_w, wh - LIST_TOP - 20)
    img = pyautogui.screenshot(region=region)
    img.save(filename)
    print(f"  [面板截图] 已保存: {filename}  区域={region}")
    return img, region


def click_row(hwnd, row_index):
    """点击搜索结果列表第 row_index 行（0-based）"""
    wx, wy, ww, wh = get_win_rect(hwnd)
    panel_w = min(PANEL_WIDTH, ww // 3)
    cx = wx + panel_w // 2
    cy = wy + LIST_TOP + row_index * ITEM_HEIGHT + ITEM_HEIGHT // 2
    print(f"  [点击] 第{row_index}行: ({cx}, {cy})")
    pyautogui.click(cx, cy)
    return cx, cy


# ══════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════

# 1. 找到微信主窗口并激活
hwnd = user32.FindWindowW("WeChatMainWnd", None)
if hwnd == 0:
    hwnd = user32.FindWindowW(None, "微信")
if hwnd == 0:
    raise RuntimeError("未找到微信窗口，请先打开微信！")
print(f"微信窗口 hwnd: {hwnd}")

user32.ShowWindow(hwnd, 9)   # SW_RESTORE
user32.SetForegroundWindow(hwnd)
time.sleep(1.5)

pyautogui.screenshot("step1_init.png")
print("截图1: 初始状态")

# 2. Ctrl+F 打开搜索框
pyautogui.hotkey('ctrl', 'f')
time.sleep(1.5)
pyautogui.screenshot("step2_search_open.png")
print("截图2: 搜索框打开")

# 3. 输入目标群名，等待搜索结果加载
pyperclip.copy(TARGET_GROUP)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(SEARCH_WAIT)
pyautogui.screenshot("step3_search_result.png")
print("截图3: 搜索结果（完整）")

# 额外截取左侧面板，便于调试确认
capture_search_panel(hwnd, "debug_panel.png")

# 4. 精确点击目标群聊
#    微信搜索结果：第0行通常是"搜索"跳转项，第1行才是第一个真实结果
#    但实际布局因版本而异 —— 先点第0行，再试第1行
print(f"\n>>> 定位目标群聊: [{TARGET_GROUP}]")
click_row(hwnd, row_index=0)

time.sleep(2)
pyautogui.screenshot("step4_after_enter.png")
print("截图4: 点击搜索结果后")

time.sleep(0.8)
pyautogui.screenshot("step5_ready_to_type.png")
print("截图5: 准备输入")

# 5. 点击聊天输入框
wx, wy, ww, wh = get_win_rect(hwnd)
print(f"微信窗口位置: x={wx}, y={wy}, w={ww}, h={wh}")

input_x = wx + ww // 2
input_y = wy + int(wh * 0.88)
print(f"点击输入框位置: ({input_x}, {input_y})")
pyautogui.click(input_x, input_y)
time.sleep(0.8)
pyautogui.screenshot("step6_clicked_input.png")
print("截图6: 点击输入框后")

# 6. 输入消息
pyperclip.copy(MESSAGE)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.8)
pyautogui.screenshot("step7_typed.png")
print("截图7: 输入消息后")

# 7. 发送
pyautogui.press('enter')
time.sleep(1)
pyautogui.screenshot("step8_sent.png")
print("截图8: 发送后")

print("\n操作完成！截图已保存到当前目录")
print("请检查 debug_panel.png 确认搜索结果面板内容是否正确。")
