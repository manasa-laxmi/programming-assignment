from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

options = UiAutomator2Options()
options.platform_name = "Android"
options.set_capability("appium:deviceName", "Android")
options.set_capability("appium:appPackage", "com.makemytrip")
options.set_capability("appium:appActivity", "com.makemytrip.ui.launch.SplashActivity")

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(5)

# Tap Flights
driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Flights']").click()
time.sleep(3)

# From
driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'From')]").click()
time.sleep(2)
driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("Hyderabad")
time.sleep(2)

# To
driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'To')]").click()
time.sleep(2)
driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("Delhi")

time.sleep(5)
driver.quit()
