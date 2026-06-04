# Test Cases — Minimal Todo (Android)
**Framework:** Appium + Python + pytest  
**Package:** `com.example.avjindersinghsekhon.minimaltodo`

---

## Features ที่ test (จาก source code จริง)

| ID | Feature | Test Case | Expected Result |
|----|---------|-----------|-----------------|
| TC-01 | Add Todo | กด FAB แล้วพิมพ์ข้อความ | task ปรากฏใน RecyclerView |
| TC-02 | Add Todo | เพิ่มหลาย task | ทุก task ปรากฏครบ |
| TC-03 | Add Todo | item ที่เพิ่มมี color dot | `toDoListItemColorImageView` แสดง |
| TC-04 | UI | FAB ปรากฏบนหน้าหลัก | FAB `is_displayed() == True` |
| TC-05 | Delete | Swipe ซ้ายบน item | task หายออกจาก list |
| TC-06 | Delete | กด UNDO บน Snackbar | task กลับมาใน list |
| TC-07 | Reminder | เปิดหน้า Add มี checkbox | `toDoHasDateCheckBox` แสดง |
| TC-08 | Reminder | เช็ค checkbox | Date Picker Dialog ปรากฏ |
| TC-09 | Settings | กด menu → Settings | Preferences screen เปิดได้ |
| TC-10 | Night Mode | Toggle dark mode | UI เปลี่ยนธีม |
| TC-11 | Edge Case | fresh install list ว่าง | items count == 0 |
| TC-12 | Edge Case | text ยาวมาก | truncate ไม่ overflow |
| TC-13 | Persistence | ปิด-เปิด app | data ยังอยู่ |

---

## วิธี Setup และ Run

```bash
# 1. ติดตั้ง dependencies
pip install appium-python-client pytest

# 2. ติดตั้ง Appium
npm install -g appium
appium driver install uiautomator2

# 3. เปิด Android Emulator แล้วติดตั้ง APK
adb install MinimalTodo.apk

# 4. เริ่ม Appium server
appium

# 5. รัน tests
pytest test_minimal_todo.py -v
```
