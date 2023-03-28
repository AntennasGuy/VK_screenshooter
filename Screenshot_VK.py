"""
Программа заходит на страницу VK цели и делает скриншоты всей ленты до конца в отдельную папку. На последнем посте
прекращает работу.
TODO - прикрутить фейковый юзерагент или обойти капчу (после ряда использования VK даёт капчу)
TODO - https://seolik.ru/user-agents-list - это список актуальных юзер агентов.
"""

import os
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


# Заготовка для фейкового юзерагента - скорее всего здесь он неудобен
# def faker():
#     global options
#     options = Options()
#     ua = UserAgent(browsers=['chrome'])
#     user_agent = ua.random
#     print(user_agent)
#     options.add_argument(f'user-agent={user_agent}')


def cook():
    """
    Основная функция, где происходит изначальная магия кулинарии.
    Args:
        login_browser: основной объект программы (браузер)
        link: ссылка на страницу клиента
        shema(str): это имя пользователя (цели) и запись для имени папки и в файлах
    :return: None
    """
    print('♫♫♫ Эта программа для сбора скриншотов со страницы в VK ♫♫♫')
    print('=============================================================', end='\n')
    global login_browser, shema
    link = input("► Вставьте, пожалуйста, адрес целевой страницы в VK (адрес профиля): ")
    shema = link.split('/')[-1]

    login_browser = webdriver.Chrome()
    login_browser.maximize_window()  # важно максимизировать окно - могут быть проблемы с мобильной версией
    login_browser.get(f"{link}")

    while True:  # простая проверка на существующую уже папку с подобным именем, чтобы программа не прерывалась
        try:
            os.mkdir(shema)
            break
        except FileExistsError:
            print('Данная папка уже существует!')
            break


def difference_images(img1, img2):
    """
    Функция для сравнения скриншотов. Служит для остановки процесса сбора изображений. Если последняя картинка и
    предидущая равны по размеру - программа заканчивается (функция возвращает True).
    :param img1: первая картинка
    :param img2: вторая картинка
    :return: тру или фальш
    """
    size_file_1 = os.path.getsize(img1)
    size_file_2 = os.path.getsize(img2)
    if size_file_1 == size_file_2:
        # print(img1, img2, 'Картинки подходят')
        os.remove(img2)
        return True
    else:
        return False


def get_page():
    """
    Функция для того чтобы добраться до целевой страницы. Собственно здесь вся работа Selenium.
    Сначала спрашиваем логин и пароль своей страницы, так как нельзя парсить без ввода данных в VK.
    Здесь использовал крайне полезную фичу ActionChain для последовательного ввода команд.
    :return:
    """
    print("...Спрашиваю данные (должно появиться окно для ввода)...")
    print("► Внимание! Для безопасности пароль и логин при вставке или вводе не видны!")

    # здесь мы вводим логин и пароль через GUI
    while True:
        login = pyautogui.password(text='Введите свой логин от VK', title='Ввод логина', default='', mask='*')
        if login != None:
            break
    while True:
        password = pyautogui.password(text='Введите пароль от своей страницы VK',
                                      title='Ввод пароля', default='', mask='*')
        if password != None:
            break

    # фокусируемся на форме с кнопкой и нажимаем кнопку
    focus = login_browser.find_element(By.ID, "side_bar_inner")
    login_browser.execute_script("return arguments[0].scrollIntoView(true);", focus)
    enter_button = login_browser.find_element(By.CLASS_NAME, "quick_login_button")
    ActionChains(login_browser).click(enter_button).perform()
    time.sleep(2)

    # попадаем на окно для ввода мыла - вводим
    index_mail = login_browser.find_element(By.ID, "index_email")
    ActionChains(login_browser).click(index_mail).send_keys(login).send_keys(Keys.ENTER).perform()
    time.sleep(4)

    # попадаем на окно для ввода пароля - вводим
    password_input = login_browser.find_element(By.NAME, 'password')
    ActionChains(login_browser).click(password_input).send_keys(password).send_keys(Keys.ENTER).perform()
    time.sleep(5)


def scrolling():
    """
    Скролинговая функция. Просто служит для прокрутки страницы.
    Args:
        scroll_size: высота окна браузера - нужно для нормального скрола
        file_prefix: префикс для имени сохраняемых скриншотов
    :return:
    """
    scroll_size = login_browser.execute_script("return window.innerHeight")
    file_prefix = 0

    while True:
        file_prefix += 1
        login_browser.get_screenshot_as_file(f"./{shema}/{shema}_shot_{file_prefix}.png")
        login_browser.execute_script(f"window.scrollBy(0,{scroll_size - 100} )")
        time.sleep(1)
        if file_prefix > 2:  # если файлов уже больше двух, то можно проводить проверку на конец страницы
            if difference_images(f"./{shema}/{shema}_shot_{file_prefix}.png", f"./{shema}/{shema}"
                                                                              f"_shot_{file_prefix - 1}.png"):
                break


if __name__ == '__main__':
    cook()
    get_page()
    scrolling()
    print()
    print("Программа завершила свою работу.")
