from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from datetime import datetime, time
from re import findall
import pprint
import os


WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]


class Day:
    def __init__(self, date: str) -> None:
        self.day = datetime.strptime(date, "%d.%m.%Y")
        self.pars = []

    def add_par(self, par: str, _time: time) -> None:
        self.pars.append({"par": par, "time": _time})

    def __repr__(self) -> str:
        return f"{self.day} - {self.pars}"


def main(login: str, password: str):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.lk.sut.ru/")
    login: WebElement = driver.find_element(by=By.ID, value="users")
    login.send_keys(login)
    password: WebElement = driver.find_element(by=By.ID, value="parole")
    password.send_keys(password)
    sleep(1)
    driver.find_element(by=By.ID, value="logButton").click()
    sleep(1)
    # find element by class title_item and click on it
    driver.find_element(by=By.CLASS_NAME, value="title_item").click()
    # find element by class l_menu_a and clcik on it
    sleep(0.5)
    driver.find_element(by=By.CLASS_NAME, value="l_menu_a").click()
    sleep(1)
    # find element by style text-shadow:none;
    table = driver.find_element(by=By.CSS_SELECTOR, value='[style="text-shadow:none;"]')
    sleep(1)
    
    week = []
    for row in table.find_elements(by=By.TAG_NAME, value="tr"):
        # print(f"{row.text} !")
        if any(day in row.text for day in WEEK_DAYS):
            day = Day(row.text.split("\n")[1])
            week.append(day)
            del day
            # print("-----------------")
        else:
            # print(findall(r'\d?\d?:\d?\d?', row.text.split('\n')[0])[0])
            print(row.text)
            week[-1].add_par(
                ' '.join(row.text.split("\n")[0].split(" ")[2:]),
                time(
                    int(
                        findall(r"\d+:\d+", row.text.split("\n")[0])[0].split(
                            ":"
                        )[0]
                    ),
                    int(
                        findall(r"\d+:\d+", row.text.split("\n")[0])[0].split(
                            ":"
                        )[1]
                    ),
                ),
            )
            # regex for 9:00-10:35

            # week[-1].add_par(row.text.split('\n')[2], row.text.split('\n')[3])
        # day.add_par(row.text.split('\n')[2], row.text.split('\n')[3])
        # if row has align to left add it to pars
        # if row.get_attribute('align') == 'left':
        #     pars.append(row.text)
        # print(row.value_of_css_property('align'))
        # print(row.text)
    pprint.pprint(week)
    print(len(week))

    # print('-----------------')
    # print(pars)


if __name__ == "__main__":
    login = os.environ.get("login")
    password = os.environ.get("password")
    main("login", "password")
