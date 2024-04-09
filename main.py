from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytesseract
from PIL import Image, ImageDraw


def screenshot(url, title):
    web = 'https://' + url
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--hide-scrollbars")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(web)
    print(driver.get_screenshot_as_file(f'{title}.png'))
    driver.quit()


def detect_title(title):
    global data, image_copy
    image = Image.open(f"{title}.png")
    image_copy = image.copy()
    target_word = title
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    word_occurences = [i for i, word in enumerate(data["text"]) if word.lower() == target_word]

    for occ in word_occurences:
        blur_words(occ, title)


def blur_words(occ, title):
    w = data["width"][occ]
    h = data["height"][occ]
    l = data["left"][occ]
    t = data["top"][occ]
    p1 = (l, t)
    p2 = (l + w, t)
    p3 = (l + w, t + h)
    p4 = (l, t + h)
    draw = ImageDraw.Draw(image_copy)
    draw.rectangle((*p1, *p3))
    image_copy.save(f"{title}_copy.png")


detect_title('github')
