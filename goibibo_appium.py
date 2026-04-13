import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options as AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ── Capabilities ──────────────────────────────────────────────────────────────
options = AppiumOptions()
options.platform_name = "Android"
options.set_capability("appium:deviceName",           "R5CT20YLF0A")
options.set_capability("appium:platformVersion",      "14")
options.set_capability("appium:appPackage",           "com.goibibo")
options.set_capability("appium:appActivity",          "com.goibibo.common.HomeActivity")
options.set_capability("appium:automationName",       "UiAutomator2")
options.set_capability("appium:noReset",              False)
options.set_capability("appium:fullReset",            False)
options.set_capability("appium:dontStopAppOnReset",   True)
options.set_capability("appium:autoGrantPermissions", True)
options.set_capability("appium:newCommandTimeout",    180)
options.set_capability("appium:skipServerInstallation", True)

APPIUM_SERVER = "http://127.0.0.1:4723"
WAIT          = 20


class GoibiboFlightTest(unittest.TestCase):

    def setUp(self):
        self.driver     = webdriver.Remote(APPIUM_SERVER, options=options)
        self.wait       = WebDriverWait(self.driver, WAIT)
        self.steps      = 0
        self.start_time = None

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def tap(self, el, label=""):
        el.click()
        self.steps += 1
        if label:
            print(f"  [step {self.steps}] {label}")

    def find_and_tap(self, by, locator, label=""):
        el = self.wait.until(EC.element_to_be_clickable((by, locator)))
        self.tap(el, label or locator)
        return el

    def find_and_type(self, by, locator, text, label=""):
        el = self.wait.until(EC.presence_of_element_located((by, locator)))
        el.clear()
        el.send_keys(text)
        self.steps += 1
        print(f"  [step {self.steps}] Typed '{text}' → {label or locator}")
        return el

    def try_dismiss(self, xpaths):
        for xp in xpaths:
            try:
                el = self.driver.find_element(AppiumBy.XPATH, xp)
                el.click()
                self.steps += 1
                print("  [popup dismissed]")
                time.sleep(0.5)
            except NoSuchElementException:
                pass

    def test_book_flight(self):
        print("\n" + "="*55)
        print("  Goibibo: HYD → DEL  |  15 Jun 2026  |  1 Adult")
        print("="*55)

        # ── Phase 1: Home Screen ──────────────────────────────────────────────
        print("\n[Phase 1] Home Screen")
        self.wait.until(EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.widget.TextView[@text="Flights"]'
            '| //android.widget.TextView[contains(@text,"Flight")]'
        )))
        self.start_time = time.time()
        print("  ✓ Home screen ready — timer started")

        # Dismiss any startup popups
        self.try_dismiss([
            '//android.widget.ImageView[@content-desc="Close" or @content-desc="close"]',
            '//android.widget.Button[@text="DISMISS" or @text="Dismiss"]',
            '//android.widget.TextView[@text="DISMISS" or @text="Dismiss"]',
            '//android.widget.TextView[@text="Skip" or @text="SKIP"]',
        ])
        time.sleep(1)

        # ── Phase 2: Tap Flights tile ─────────────────────────────────────────
        print("\n[Phase 2] Tap Flights")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[@text="Flights"]',
            "Flights tile")
        time.sleep(2)

        self.try_dismiss([
            '//android.widget.TextView[@text="Skip" or @text="SKIP"]',
            '//android.widget.TextView[@text="Not Now" or @text="NOT NOW"]',
            '//android.widget.Button[@text="OK" or @text="Got it"]',
        ])

        self.wait.until(EC.presence_of_element_located((
            AppiumBy.ID, "com.goibibo:id/search_button_flat")))
        print("  ✓ Flight Search page loaded")
        time.sleep(1)

        # ── Phase 3: FROM = Hyderabad ─────────────────────────────────────────
        print("\n[Phase 3] Set Origin = Hyderabad")
        self.find_and_tap(AppiumBy.ID,
            "com.goibibo:id/from_selection_layout",
            "FROM field")
        time.sleep(1)

        self.find_and_type(AppiumBy.XPATH,
            '//android.widget.EditText',
            "hyd", "origin search box")
        time.sleep(1.5)

        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"Hyderabad")]'
            '[contains(@text,"India") or contains(@text,"HYD") or contains(@text,"Rajiv")]',
            "Hyderabad, India")
        time.sleep(1)

        # ── Phase 4: TO = New Delhi ───────────────────────────────────────────
        print("\n[Phase 4] Set Destination = New Delhi")
        try:
            dest_box = self.wait.until(EC.presence_of_element_located((
                AppiumBy.XPATH, '//android.widget.EditText')))
            dest_box.clear()
            dest_box.send_keys("del")
            self.steps += 1
            print(f"  [step {self.steps}] Typed 'del' → destination search box")
        except TimeoutException:
            self.find_and_tap(AppiumBy.ID,
                "com.goibibo:id/to_city_layout", "TO field")
            time.sleep(0.5)
            self.find_and_type(AppiumBy.XPATH,
                '//android.widget.EditText', "del", "destination search box")
        time.sleep(1.5)

        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"New Delhi")]'
            '[contains(@text,"India") or contains(@text,"DEL") or contains(@text,"Indira")]',
            "New Delhi, India")
        time.sleep(1)

        # ── Phase 5: Date = 15 June 2026 ─────────────────────────────────────
        # ── Phase 5: Date = 15 June 2026 ─────────────────────────────────────
        # ── Phase 5: Date = 15 June 2026 ─────────────────────────────────────
        print("\n[Phase 5] Set Date = 15 June 2026")
        self.find_and_tap(AppiumBy.ID,
            "com.goibibo:id/from_date_layout",
            "Departure Date field")
        time.sleep(1.5)

       # Swipe until June header is visible (your original working approach)
        print("  Scrolling to June 2026...")
        for _ in range(15):
            try:
                self.driver.find_element(AppiumBy.XPATH,
                    '//android.widget.TextView[contains(@text,"June")]')
                print("  ✓ June found")
                break
            except NoSuchElementException:
                self.driver.swipe(540, 1200, 540, 900, 800)
                time.sleep(0.8)

       # Long swipe so June moves to top and its rows are visible
        print("  Bringing June rows into view...")
        self.driver.swipe(540, 1400, 540, 600, 800)
        time.sleep(0.8)
        # Get June's position and tap 15 relative to it
        june = self.driver.find_element(AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"June")]')
        june_y = june.location['y']
        june_x = june.location['x']

        # 15 is in row 3 (after header), leftmost column (Monday)
        # row height ≈ 80px, header ≈ 60px
        tap_x = june_x + 45
        tap_y = june_y + 180  # tuned: skip header + 2 full rows
        print(f"  Tapping June 15 at ({tap_x}, {tap_y})")
        self.driver.tap([(tap_x, tap_y)])
        self.steps += 1
        print(f"  [step {self.steps}] June 15")
        time.sleep(0.5)

        time.sleep(0.5)

        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.Button[@text="DONE" or @text="Done"]'
            '| //android.widget.TextView[@text="DONE" or @text="Done"]',
            "DONE")
        time.sleep(1)

        # ── Phase 6: Search Flights ───────────────────────────────────────────
        print("\n[Phase 6] Search Flights")
        self.find_and_tap(AppiumBy.ID,
            "com.goibibo:id/search_button_flat",
            "SEARCH FLIGHTS")
        print("  Waiting for results...")
        time.sleep(7)

        self.wait.until(EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"₹")]')))
        print("  ✓ Results loaded")

        # Dismiss "Preferred Flights" popup
        time.sleep(2)
        self.try_dismiss([
            '//android.widget.TextView[@text="DISMISS" or @text="Dismiss"]',
            '//android.widget.Button[@text="DISMISS" or @text="Dismiss"]',
        ])

        # ── Phase 7: Tap first flight ─────────────────────────────────────────
        print("\n[Phase 7] Select First (Cheapest) Flight")
        prices = self.driver.find_elements(AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"₹")]')
        if prices:
            print(f"  Cheapest price visible: {prices[0].text}")

        first_flight = self.wait.until(EC.element_to_be_clickable((
            AppiumBy.XPATH,
            '(//android.view.ViewGroup[.//android.widget.TextView[contains(@text,"₹")]])[1]'
            '| (//android.widget.RelativeLayout[.//android.widget.TextView[contains(@text,"₹")]])[1]'
        )))
        self.tap(first_flight, "First (cheapest) flight card")
        time.sleep(2)

        # ── Phase 8: BOOK NOW ─────────────────────────────────────────────────
        print("\n[Phase 8] Book Now")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.Button[@text="BOOK NOW" or @text="Book Now"]'
            '| //android.widget.TextView[@text="BOOK NOW" or @text="Book Now"]',
            "BOOK NOW")
        time.sleep(2)

        # ── Phase 9: Booking Policies → CONTINUE ─────────────────────────────
        print("\n[Phase 9] Booking Policies → CONTINUE")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.Button[@text="CONTINUE" or @text="Continue"]'
            '| //android.widget.TextView[@text="CONTINUE" or @text="Continue"]',
            "CONTINUE")
        time.sleep(2)

        # ── Phase 10: Add Traveller ───────────────────────────────────────────
        # ── Phase 10: Add Traveller ───────────────────────────────────────────
        print("\n[Phase 10] Add Traveller Details")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[@text="Add new adult"]'
            '| //android.widget.Button[@text="Add new adult"]',
            "Add new adult")
        time.sleep(1.5)

        # Gender
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[@text="MALE" or @text="Male"]'
            '| //android.widget.Button[@text="MALE" or @text="Male"]',
            "MALE")
        time.sleep(0.5)

                # First name
        fn = self.wait.until(EC.element_to_be_clickable((
            AppiumBy.XPATH, '//android.widget.EditText[contains(@hint,"First") or contains(@hint,"first")]')))
        fn.click()
        time.sleep(0.3)
        self.driver.execute_script('mobile: type', {'text': 'ram'})
        self.steps += 1
        print(f"  [step {self.steps}] Typed 'ram' → First Name")

        # Press back to close keyboard and defocus
        self.driver.press_keycode(4)  # KEYCODE_BACK
        time.sleep(0.5)

        # Last name
        ln = self.wait.until(EC.element_to_be_clickable((
            AppiumBy.XPATH, '//android.widget.EditText[contains(@hint,"Last") or contains(@hint,"last")]')))
        ln.click()
        time.sleep(0.3)
        self.driver.execute_script('mobile: type', {'text': 'gandhi'})
        self.steps += 1
        print(f"  [step {self.steps}] Typed 'gandhi' → Last Name")

        # Press back to close keyboard
        self.driver.press_keycode(4)  # KEYCODE_BACK
        time.sleep(0.5)

        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.Button[@text="CONFIRM" or @text="Confirm"]'
            '| //android.widget.TextView[@text="CONFIRM" or @text="Confirm"]',
            "CONFIRM traveller")
        time.sleep(1.5)

        # ── Phase 11: Contact Details ─────────────────────────────────────────
        print("\n[Phase 11] Add Contact Details")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[contains(@text,"Add Email")]'
            '| //android.widget.TextView[contains(@text,"email")]',
            "Add Email ID")
        time.sleep(1)

        self.find_and_type(AppiumBy.XPATH,
            '(//android.widget.EditText)[1]',
            "testuser@gmail.com", "Email")
        time.sleep(0.5)

        # Clear existing number and type new one
        try:
            phone_el = self.driver.find_element(AppiumBy.XPATH,
                '(//android.widget.EditText)[2]')
            phone_el.clear()
            phone_el.send_keys("9876543210")
            self.steps += 1
            print(f"  [step {self.steps}] Typed phone number")
        except NoSuchElementException:
            pass
        time.sleep(0.5)

        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.Button[@text="CONFIRM" or @text="Confirm"]'
            '| //android.widget.TextView[@text="CONFIRM" or @text="Confirm"]',
            "CONFIRM contact")
        time.sleep(1.5)

        # ── Phase 12: CONTINUE ────────────────────────────────────────────────
            # ── Phase 12b: Check Save Details and Continue ────────────────────────
        print("\n[Phase 12b] Check Save Details and Continue")
        time.sleep(1.5)

        # Scroll checkbox into view using UiAutomator
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().resourceId("com.goibibo:id/confirmationCheckBox"))'
        )
        time.sleep(0.5)

        # Tick the checkbox
        checkbox = self.wait.until(EC.element_to_be_clickable((
            AppiumBy.ID, "com.goibibo:id/confirmationCheckBox")))
        checkbox.click()
        self.steps += 1
        print(f"  [step {self.steps}] Checked 'Save these details to my profile'")
        time.sleep(0.5)

        # Tap CONTINUE
        self.find_and_tap(AppiumBy.ID,
            "com.goibibo:id/review_tv",
            "CONTINUE")
        time.sleep(2)


        # ── Phase 13: Trip Protection → Travel Unsecured ──────────────────────
        print("\n[Phase 13] Trip Protection popup")
        time.sleep(2)
        self.try_dismiss([
            '//android.widget.TextView[@text="Travel Unsecured" or @text="TRAVEL UNSECURED"]',
            '//android.widget.Button[@text="Travel Unsecured" or @text="TRAVEL UNSECURED"]',
        ])
        time.sleep(1)

        # ── Phase 14: Review Details → CONFIRM ───────────────────────────────
        print("\n[Phase 14] Review Details")
        time.sleep(2)
        self.try_dismiss([
            '//android.widget.TextView[@text="CONFIRM" or @text="Confirm"]',
            '//android.widget.Button[@text="CONFIRM" or @text="Confirm"]',
        ])
        time.sleep(2)

        # ── Phase 15: Add-ons → Skip To Payment ──────────────────────────────
        print("\n[Phase 15] Add-ons → Skip To Payment")
        self.find_and_tap(AppiumBy.XPATH,
            '//android.widget.TextView[@text="Skip To Payment" or @text="SKIP TO PAYMENT"]'
            '| //android.widget.Button[@text="Skip To Payment" or @text="SKIP TO PAYMENT"]',
            "Skip To Payment")
        time.sleep(3)

        # ── Phase 16: Verify Payment Page ────────────────────────────────────
        print("\n[Phase 16] Verify Payment Page")
        self.wait.until(EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.widget.TextView[@text="Payment" or @text="PAYMENT"]'
            '| //android.widget.TextView[contains(@text,"Total Due")]'
            '| //android.widget.TextView[contains(@text,"Payment Options")]'
        )))
        print("  ✅ Payment page reached! Stopping as required.")

        # ── Final Report ──────────────────────────────────────────────────────
        t = time.time() - self.start_time
        print(f"\n{'='*55}")
        print(f"  GOIBIBO — FINAL REPORT")
        print(f"{'='*55}")
        print(f"  Route      : Hyderabad → New Delhi")
        print(f"  Date       : 15 June 2026 | 1 Adult | Economy")
        print(f"  Total Steps: {self.steps}")
        print(f"  Total Time : {t:.2f}s  ({int(t//60):02d}m {int(t%60):02d}s)")
        print(f"{'='*55}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
