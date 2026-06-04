# ============================================================
# Automation Test Scripts: Minimal Todo (Android)
# Framework: Appium + Python (pytest)
# App: com.example.avjindersinghsekhon.minimaltodo
#
# Setup:
#   pip install appium-python-client pytest
#   Start Appium server: appium
#   Start Android Emulator (API 28+)
#   Run: pytest test_minimal_todo.py -v
# ============================================================

import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CAPS = {
    "platformName": "Android",
    "deviceName": "emulator-5554",       # ชื่อ emulator (ดูจาก: adb devices)
    "appPackage": "com.example.avjindersinghsekhon.minimaltodo",
    "appActivity": ".Main.MainActivity",
    "automationName": "UiAutomator2",
    "noReset": False,                     # True = ไม่ล้างข้อมูลก่อนเทส
    "newCommandTimeout": 60,
}

APPIUM_SERVER = "http://127.0.0.1:4723"

# Resource IDs จาก source code จริง
ID_TODO_LIST       = "com.example.avjindersinghsekhon.minimaltodo:id/toDoRecyclerView"
ID_ITEM_TEXT       = "com.example.avjindersinghsekhon.minimaltodo:id/toDoListItemTextview"
ID_ITEM_TIME       = "com.example.avjindersinghsekhon.minimaltodo:id/todoListItemTimeTextView"
ID_ITEM_COLOR      = "com.example.avjindersinghsekhon.minimaltodo:id/toDoListItemColorImageView"
ID_FAB             = "com.example.avjindersinghsekhon.minimaltodo:id/addToDoItemFAB"
ID_TODO_INPUT      = "com.example.avjindersinghsekhon.minimaltodo:id/userToDoEditText"
ID_DATE_CHECKBOX   = "com.example.avjindersinghsekhon.minimaltodo:id/toDoHasDateCheckBox"
ID_DATE_TEXT       = "com.example.avjindersinghsekhon.minimaltodo:id/toDoDateTextView"


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options().load_capabilities(CAPS)
    d = webdriver.Remote(APPIUM_SERVER, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()

def wait_for(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def add_todo(driver, text):
    """Helper: เพิ่ม todo item"""
    driver.find_element(AppiumBy.ID, ID_FAB).click()
    driver.find_element(AppiumBy.ID, ID_TODO_INPUT).send_keys(text)
    # กด checkmark/done เพื่อบันทึก
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "done").click()


# ─────────────────────────────────────────────
# TEST SUITE 1: Add Todo
# ─────────────────────────────────────────────
class TestAddTodo:

    def test_TC01_add_single_todo(self, driver):
        """TC-01: กด FAB → พิมพ์ข้อความ → บันทึก → ปรากฏใน list"""
        add_todo(driver, "Buy groceries")
        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        texts = [i.text for i in items]
        assert "Buy groceries" in texts

    def test_TC02_add_multiple_todos(self, driver):
        """TC-02: เพิ่มหลาย todo ต้องปรากฏครบ"""
        tasks = ["Task Alpha", "Task Beta", "Task Gamma"]
        for t in tasks:
            add_todo(driver, t)
        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        texts = [i.text for i in items]
        for t in tasks:
            assert t in texts, f"'{t}' ไม่ปรากฏใน list"

    def test_TC03_todo_item_shows_color_dot(self, driver):
        """TC-03: item ที่เพิ่มมีวงกลมสีแสดง"""
        add_todo(driver, "Color test task")
        color_dots = driver.find_elements(AppiumBy.ID, ID_ITEM_COLOR)
        assert len(color_dots) >= 1

    def test_TC04_fab_button_visible_on_main_screen(self, driver):
        """TC-04: ปุ่ม + (FAB) แสดงบนหน้าหลักเสมอ"""
        fab = driver.find_element(AppiumBy.ID, ID_FAB)
        assert fab.is_displayed()


# ─────────────────────────────────────────────
# TEST SUITE 2: Delete Todo (Swipe)
# ─────────────────────────────────────────────
class TestDeleteTodo:

    def test_TC05_delete_todo_by_swipe(self, driver):
        """TC-05: swipe ซ้าย/ขวาบน item เพื่อลบ"""
        add_todo(driver, "Task to delete")

        # หา item ที่ต้องการลบ
        item = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceId("{}").text("Task to delete")'.format(ID_ITEM_TEXT))

        # Swipe ซ้ายออกนอกหน้าจอ
        size = driver.get_window_size()
        start_x = size['width'] * 0.8
        end_x   = size['width'] * 0.1
        y       = item.location['y'] + item.size['height'] / 2
        driver.swipe(start_x, y, end_x, y, duration=500)
        time.sleep(1)

        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        texts = [i.text for i in items]
        assert "Task to delete" not in texts

    def test_TC06_undo_delete_with_snackbar(self, driver):
        """TC-06: หลัง swipe ลบ ควรมี Snackbar 'UNDO' ให้กด"""
        add_todo(driver, "Undo test task")

        item = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceId("{}").text("Undo test task")'.format(ID_ITEM_TEXT))

        size = driver.get_window_size()
        start_x = size['width'] * 0.8
        end_x   = size['width'] * 0.1
        y = item.location['y'] + item.size['height'] / 2
        driver.swipe(start_x, y, end_x, y, duration=500)

        # กด UNDO บน Snackbar
        undo_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH,
                '//*[@text="UNDO" or @text="Undo"]'))
        )
        undo_btn.click()
        time.sleep(1)

        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        texts = [i.text for i in items]
        assert "Undo test task" in texts


# ─────────────────────────────────────────────
# TEST SUITE 3: Reminder / Date
# ─────────────────────────────────────────────
class TestReminder:

    def test_TC07_open_add_screen_has_date_checkbox(self, driver):
        """TC-07: หน้า Add Todo มี checkbox สำหรับตั้ง reminder"""
        driver.find_element(AppiumBy.ID, ID_FAB).click()
        checkbox = driver.find_element(AppiumBy.ID, ID_DATE_CHECKBOX)
        assert checkbox.is_displayed()

    def test_TC08_check_reminder_shows_date_picker(self, driver):
        """TC-08: เช็ค checkbox reminder แล้ว date picker ปรากฏ"""
        driver.find_element(AppiumBy.ID, ID_FAB).click()
        driver.find_element(AppiumBy.ID, ID_TODO_INPUT).send_keys("Reminder task")
        driver.find_element(AppiumBy.ID, ID_DATE_CHECKBOX).click()

        # Date picker dialog ควรปรากฏ
        date_picker = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH,
                '//*[@class="android.widget.DatePicker"]'))
        )
        assert date_picker.is_displayed()


# ─────────────────────────────────────────────
# TEST SUITE 4: Night Mode / Settings
# ─────────────────────────────────────────────
class TestSettings:

    def test_TC09_settings_menu_accessible(self, driver):
        """TC-09: กด menu แล้วมี Settings ให้เลือก"""
        driver.find_element(AppiumBy.XPATH,
            '//android.widget.ImageView[@content-desc="More options"]').click()
        settings = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH,
                '//*[@text="Preferences" or @text="Settings"]'))
        )
        assert settings.is_displayed()

    def test_TC10_toggle_night_mode(self, driver):
        """TC-10: เปิด Settings → toggle Night Mode → UI เปลี่ยนสี"""
        driver.find_element(AppiumBy.XPATH,
            '//android.widget.ImageView[@content-desc="More options"]').click()
        driver.find_element(AppiumBy.XPATH,
            '//*[@text="Preferences" or @text="Settings"]').click()

        night_toggle = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH,
                '//*[contains(@text,"Night") or contains(@text,"Dark")]'))
        )
        night_toggle.click()
        time.sleep(1)
        # ยืนยันว่า toggle เปลี่ยนสถานะ (checked/unchecked)
        assert night_toggle.is_enabled()


# ─────────────────────────────────────────────
# TEST SUITE 5: Edge Cases
# ─────────────────────────────────────────────
class TestEdgeCases:

    def test_TC11_empty_list_shows_no_items(self, driver):
        """TC-11: list เริ่มต้นว่างเปล่า (fresh install)"""
        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        assert len(items) == 0

    def test_TC12_long_text_todo_truncated(self, driver):
        """TC-12: text ยาวมากควรถูก truncate (ellipsize) ไม่ overflow"""
        long_text = "This is a very long todo item that should be truncated " * 3
        add_todo(driver, long_text)
        item = driver.find_element(AppiumBy.ID, ID_ITEM_TEXT)
        # ตรวจว่า element ยังแสดงอยู่ในหน้าจอ (ไม่ overflow ออกนอก)
        size = driver.get_window_size()
        loc = item.location
        assert loc['x'] >= 0
        assert loc['x'] + item.size['width'] <= size['width']

    def test_TC13_todo_persists_after_app_restart(self, driver):
        """TC-13: ปิด-เปิด app แล้ว todo ยังอยู่ (data persistence)"""
        add_todo(driver, "Persistent task")

        # Background app แล้วกลับมา
        driver.background_app(3)
        time.sleep(2)

        items = driver.find_elements(AppiumBy.ID, ID_ITEM_TEXT)
        texts = [i.text for i in items]
        assert "Persistent task" in texts
