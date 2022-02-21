import time  # импорты библиотек
import datetime
import pyautogui as pag
import schedule
from selenium import webdriver

from data import payload

URL = 'https://pegas.bsu.edu.ru/mod/bigbluebuttonbn/view.php?id=1136555'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
}
HOST = 'https://pegas.bsu.edu.ru/login/index.php'


def auth(payload):  # аутентификация в пегасе
    driver = webdriver.Safari()  # инициализация веб-драйвера
    # открываем страницу аутентификации
    driver.set_window_size(1440, 900)
    driver.get('https://pegas.bsu.edu.ru/login/index.php')
    username = driver.find_element_by_css_selector(
        "input#username")  # выбираем input-username
    username.click()  # кликаем по нему
    username.send_keys(payload['username'])  # и вводим логин
    password = driver.find_element_by_css_selector(
        "input#password")  # ищем input-password
    password.click()  # кликаем по нему
    password.send_keys(payload['password'])  # и вводим пароль
    # ищем button для отправки введенных данных
    submit = driver.find_element_by_css_selector("button#loginbtn")
    submit.click()  # кликаем на кнопку
    time.sleep(10)  # ожидаем прогрузку
    return driver  # возвращаем веб-драйвер для передачи его в следущую функцию


def connect(driver, url):  # получаем драйвер из функции auth
    driver.get(url)  # переходим по ссылке для подключения к конфе
    btn = driver.find_element_by_css_selector(
        "input#join_button_input")  # ищем кропку подключения к конфе
    btn.click()  # кликаем по ней
    time.sleep(5)  # ожидаем прогрузку
    return driver  # возвращаем драйвер для передачи в следущую функцию


def listen():
    pag.moveTo(800, 478)
    pag.click()
    time.sleep(2)
    pag.moveTo(721, 460)
    pag.click()
    time.sleep(5400)


def main():
    pairs = ['https://pegas.bsu.edu.ru/mod/bigbluebuttonbn/view.php?id=1136555',
             'https://pegas.bsu.edu.ru/mod/bigbluebuttonbn/view.php?id=1172547']
    for url in pairs:
        now = datetime.datetime.now()
        # print(pag.size())
        # функция выполняет аутентификацию и возвращает веб-драйвер
        driver = auth(payload)
        # полученный веб-драйвер передаем в функцию для подключения к конфе и возвращаем веб-драйвер
        connect(driver, url=url)
        listen()
        driver.quit()
        if now.strftime("%H:%M") != '14:00':
            time.sleep(1500)


if __name__ == '__main__':
    schedule.every().monday.at("12:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
