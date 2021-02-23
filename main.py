from selenium import webdriver
import time

BUTTON_BUY_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/section[3]/div[2]/form/div[2]/button"
BUTTON_PLUS_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/section[3]/div[2]/form/div[1]/button[2]/i"
AVALIBILITY_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/section[3]/div[2]/div/div"
PRICE_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[2]/td"
PRICE2_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr/td"
PRICE3_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/section[3]/div[1]/div[1]/div[2]"
TITLE_XPATH = "//*[@id=\"product_detail_content\"]/div/div[1]/div[2]/h1"
TITLE_XPATH2 = "/html/body/div[2]/div[8]/div/div/main/div/div/div/div[1]/div[2]/section[1]/h1"
REGISTER_XPATH = "//*[@id=\"skrollr-body\"]/div[2]/div[1]/div[1]/div/div[3]/div/a/span"
EMAIL_XPATH = "//*[@id=\"js-reg-popup-login\"]/div[2]/form/div[1]/input"
PASSWORD_XPATH = "//*[@id=\"js-reg-popup-login\"]/div[2]/form/div[2]/input"
BUTTON_SIGNIN_XPATH = "//*[@id=\"js-reg-popup-login\"]/div[2]/form/button"
NEDOSTUPNE = "Dočasně nedostupné"
EMAIL = "stepan.zalis@gmail.com"
PASS = "wield.crops.ago"


def is_available(driver):
    try:
        driver.find_element_by_xpath(AVALIBILITY_XPATH).text
        available = False
    except:
        available = True
    return available


def add_to_cart(driver):
    try:
        driver.find_element_by_xpath(BUTTON_BUY_XPATH).click()
    except:
        driver.find_element_by_xpath(BUTTON_PLUS_XPATH).click()


def get_title(driver):
    try:
        title = driver.find_element_by_xpath(TITLE_XPATH).text
    except :
        title = driver.find_element_by_xpath(TITLE_XPATH2).text
    return title


def get_float_price(price):
    price_split = price.split(" ")
    price_split = price_split[0].split(",")
    finalprice = float(price_split[0])
    if len(price_split) > 1:
        finalprice += float("0." + price_split[1])
    return finalprice


def get_price(driver):
    try:
        price = driver.find_element_by_xpath(PRICE3_XPATH).text
    except:
        price = driver.find_element_by_xpath(PRICE2_XPATH).text

    price = get_float_price(price)
    return price


def register(driver):
    driver.get("https://www.grizly.cz")
    driver.find_element_by_xpath(REGISTER_XPATH).click()
    # driver.find_element_by_xpath(REGISTER_XPATH).click()
    email = driver.find_element_by_xpath(EMAIL_XPATH)
    email.send_keys(EMAIL)
    password = driver.find_element_by_xpath(PASSWORD_XPATH)
    password.send_keys(PASS)
    driver.find_element_by_xpath(BUTTON_SIGNIN_XPATH).click()


class Grizlik:
    def __init__(self, name, links, total_price, unavailable, available):
        self.links = links
        self.name = name
        self.total_price = total_price
        self.unavailable = unavailable
        self.available = available

    def __str__(self):
        return self.name + "\n" + "Celková cena: " + str(self.total_price) + "\nDostupné: " + str(
            self.available) + "\nNedostuptné: " + str(self.unavailable)

    def add_to_total(self, price):
        self.total_price += price

    def add_link(self, link):
        self.links.append(link)

    def get_total(self):
        return self.total_price

    def order(self, driver):
        for link in self.links:
            driver.get(link)
            available = is_available(driver)
            price = get_price(driver)

            if available:
                add_to_cart(driver)
                self.add_to_total(price)
                title = get_title(driver)
                self.available.append("\n" + title + " " + price)
                time.sleep(3)

            if not available:
                title = get_title(driver)
                self.unavailable.append("\n" + title + " " + price)


def create_grizlici_from_file(file_name):
    with open(file_name, 'r') as file_object:
        line = file_object.readline()
        grizlik_list = []
        total_items = 0
        while line:
            if line[0] == '#':
                line = file_object.readline()
                continue
            split = line.split(";")

            if len(split) == 1:
                grizlik_list.append(Grizlik(split[0], [], 0, [], []))
                total_items += 1
            else:
                link_count = int(split[0])
                total_items += link_count
                grizlink = split[1]
                for x in range(link_count):
                    grizlik_list[-1].links.append(grizlink)

            line = file_object.readline()

        return grizlik_list, total_items


grizlici, totalItems = create_grizlici_from_file("grizlinky.txt")
options = webdriver.ChromeOptions()
options.binary_location = "/opt/google/chrome/chrome"
chrome_driver_binary = "/usr/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary)
driver.maximize_window()
register(driver)
total = 0
for gri in grizlici:
    gri.order(driver)
    total += gri.total_price
    print(gri)

print("Celková cena: " + str(total))
print("kontrolní počet položek: " + str(totalItems))
