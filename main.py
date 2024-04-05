from selenium import webdriver
from selenium.webdriver.chrome.options import Options

web = "borjomi.ru"
URL = 'https://' + web
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--hide-scrollbars")
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
print(driver.get_screenshot_as_file(f'{web.split(".")[0]}.png'))
driver.quit()
