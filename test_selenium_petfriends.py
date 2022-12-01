import pytest
import time
# Для того чтобы браузер работал
from selenium import webdriver
# Для поиска
from selenium.webdriver.common.by import By
# Для ожидания
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Автоматом запускается перед тестами для запуска браузера и открытия страницы
@pytest.fixture(autouse=True)
def testing():
    # Задаем браузер для тестов и путь к драйверу
    pytest.driver = webdriver.Chrome('D:\\books\\study\\python\\sf\\24\\chromedriver\\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Ищем поле почты и вводим ее
    pytest.driver.find_element(By.ID, 'email').send_keys('00@00.ru')
    # time.sleep(0.5)
    # Ищем поле пароля и вводим его
    pytest.driver.find_element(By.ID, 'pass').send_keys('00')
    # time.sleep(0.5)
    # Ищем кнопку входа и нажимаем ее
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # time.sleep(0.5)
    # Проверяем видимость кнопки Мои питомцы, разворачиваем, если не видно
    my_pets_button = WebDriverWait(pytest.driver, 0).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'navbar-toggler'))
    )
    if my_pets_button:
        pytest.driver.find_element(By.CLASS_NAME, 'navbar-toggler').click()
    # time.sleep(0.5)
    # Ищем ссылку Мои питомцы и нажимаем на нее
    pytest.driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # time.sleep(0.5)

    # Тут выполняются тесты
    yield

    # Закрывает браузер после тестов
    pytest.driver.quit()


# Проверяем, что мы на нужной странице
def test_show_my_pets():
    # Проверяем, что мы оказались на странице с питомцами пользователя
    assert pytest.driver.find_element(By.XPATH, '//th[1][@scope="col"]').text == "Фото"
    print('\n')
    print("Проверяем, что мы на странице питомцев пользователя.")


# Проверяем, что на странице питомцев пользователя присутствуют все питомцы
def test_visible_my_pets():
    user_inf = ''
    user_inf_pet = ''
    # Достаем данные с количеством питомцев со страницы
    for i in pytest.driver.find_elements(By.XPATH, '//div[@class=".col-sm-4 left"]'):
        user_inf = i.text.split(' ')
        user_inf_pet = user_inf[1].split('\n')
    # Считаем количество строк в таблице
    amount_row = len(pytest.driver.find_elements(By.XPATH, '//th[@scope="row"]'))
    # Сравниваем
    assert user_inf_pet[0] == str(amount_row)
    print('\n')
    print("Проверяем, что на странице питомцев пользователя присутствуют все питомцы.")


# Проверяем, что у половины питомцев (или большей части) есть фото
def test_photo():
    # Добавляем ожидание загрузки
    pytest.driver.implicitly_wait(10)
    pet_with_photo = 0
    # Берем все строки таблицы и перебором считаем в скольких есть картинки
    str_row = pytest.driver.find_elements(By.XPATH, '//th[@scope="row"]/img')
    for i in range(len(str_row)):
        if str_row[i].get_attribute('src') != '':
            pet_with_photo += 1
    # Сравниваем
    assert pet_with_photo >= len(str_row)/2
    print('\n')
    print("Проверяем, что у половины питомцев (или большей части) есть фото.")


# Проверяем, что у всех питомцев есть имя, возраст и порода
def test_pets_inf():
    # Добавляем ожидание загрузки
    pytest.driver.implicitly_wait(10)
    # Выбираем всю инфу из строк с питомцами и проверяем что она есть
    pets_inf = pytest.driver.find_elements(By.XPATH, '//th[@scope="row"]/../td')
    for i in range(len(pets_inf)):
        assert pets_inf[i].text != ''
    print('\n')
    print("Проверяем, что у всех питомцев есть имя, возраст и порода.")


# Проверяем, что у питомцев нет повторяющихся имен
def test_pets_name_not_double():
    # Выбираем всю инфу из строк с питомцами
    pets_inf = pytest.driver.find_elements(By.XPATH, '//th[@scope="row"]/../td')
    pets_inf_all = []
    # Собираем всю инфу в список
    for i in range(len(pets_inf)):
        x = pets_inf[i].text
        pets_inf_all.append(x)
    # Выбираем имена
    pets_inf_all = pets_inf_all[0::4]
    pia_count = 0
    # Считаем совпадения имен, должно получиться равным количеству питомцев
    for i in range(len(pets_inf_all)):
        for j in range(len(pets_inf_all)):
            if pets_inf_all[i] in pets_inf_all[j]:
                pia_count += 1
    # Сравниваем
    assert pia_count == len(pets_inf_all)
    print('\n')
    print("Проверяем, что у питомцев нет повторяющихся имен.")


# Проверяем, что питомцы не повторяются (т.е. нет полного повторения данных)
def test_pets_not_double():
    # Выбираем всю инфу из строк с питомцами
    pets_inf = pytest.driver.find_elements(By.XPATH, '//th[@scope="row"]/../td')
    pets_inf_all = []
    # Собираем всю инфу в список
    for i in range(len(pets_inf)):
        x = pets_inf[i].text
        pets_inf_all.append(x)
    # Убираем лишние знаки
    del pets_inf_all[3::4]
    # Добавляем запятые после каждого третьего знака, чтобы отделить данные одного питомца от другого
    x = 3
    for i in range(int(len(pets_inf_all)/3 - 1)):
        pets_inf_all.insert(x, ',')
        x += 4
    # Объединяем все в строку
    pets_inf_all = ''.join(map(str, pets_inf_all))
    # Разбиваем строку по запятой, получаем список с инфой по питомцу в отдельном элементе
    pets_inf_all = pets_inf_all.split(',')
    pia_count = 0
    # Считаем совпадения данных по питомцам, должно получиться равным количеству питомцев
    for i in range(len(pets_inf_all)):
        for j in range(len(pets_inf_all)):
            if pets_inf_all[i] in pets_inf_all[j]:
                pia_count += 1
    # Сравниваем
    assert pia_count == len(pets_inf_all)
    print('\n')
    print("Проверяем, что питомцы не повторяются (т.е. нет полного повторения данных).")
