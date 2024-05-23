# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

import os
import time

from Screenshot import Screenshot
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from logger import get_logger

logger = get_logger(__name__)
chromedrvier_path = os.getenv("CHROMEDRIVER_PATH")

def sidecar_id():
    return '#__next > div > div:nth-child(1) > div > div > div.Pane.vertical.Pane1 > div > div.style_closeBtn__rWKqG'

def fullscreen_id():
    return '#DASHBOARD_PANEL_ID > div.style_dashboardPanel__r3e0U > div.style_tabBar__RrS9Q > div.style_tabRight__91w_0 > button.sc-GhhNo.gpGkBP.style_atcButton__H4qwy' # old apitable
    # return '#DASHBOARD_PANEL_ID > div.style_dashboardPanel__r3e0U > div.style_tabBar__RrS9Q > div.style_tabRight__91w_0 > button.sc-jrcTuL.iGlphV.style_atcButton__H4qwy'  # new vikadata

def item_id(id: int):
    return f'#__next > div > div:nth-child(1) > div > div > div.Pane.vertical.Pane1 > div > div.style_shareMenu__C86Q_ > div.style_treeWrapper__vjF2w.undefined > div > div.ant-tree-list > div > div > div > div:nth-child({id})'


def screenshot(url: str, screenshot_name: str):
    ob = Screenshot.Screenshot()
    options = Options()
    options.add_argument("--headless")  # 指定使用无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速，某些系统/驱动程序可能需要
    options.add_argument("--window-size=1920x1440")  # 设置窗口大小，确保网页元素完全显示
    options.add_argument("--no-sandbox")  # 以最高权限运行
    options.add_argument("--disable-dev-shm-usage")  # 禁用/dev/shm 使用，某些系统可能需要
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-infobars")  # 禁用信息栏

    try:
        driver = webdriver.Chrome(service=Service(
            chromedrvier_path), options=options)

        # 下面是截图
        driver.get(url)
        driver.fullscreen_window()

        # 等待页面的某个元素加载完成，确保异步内容加载
        WebDriverWait(driver, 20).until(
            # EC.presence_of_element_located((By.ID, 'DATASHEET_VIEW_CONTAINER_ID'))  # 数据表
            # EC.presence_of_element_located((By.ID, 'DASHBOARD_PANEL_ID'))  # 仪表盘
            EC.presence_of_element_located(
                (By.ID, 'FOLDER_SHOWCASE_NODES_CONTAINER'))  # 文件夹
        )

        # 菜单 01
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, item_id(2)).click()

        # 等待某个元素加载完成，确保异步内容加载
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, 'DASHBOARD_PANEL_ID'))  # 替换为您需要等待加载的元素 ID
        )

        time.sleep(10)
        # 展开/折叠侧边栏
        driver.find_element(By.CSS_SELECTOR, sidecar_id()).click()
        driver.find_element(By.CSS_SELECTOR, fullscreen_id()).click()
        driver.save_screenshot('1_' + screenshot_name)

        # 菜单 02
        time.sleep(10)
        # 展开/折叠侧边栏
        driver.find_element(By.CSS_SELECTOR, fullscreen_id()).click()
        driver.find_element(By.CSS_SELECTOR, sidecar_id()).click()
        driver.find_element(By.CSS_SELECTOR, item_id(3)).click()

        # 等待某个元素加载完成，确保异步内容加载
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, 'DASHBOARD_PANEL_ID'))  # 替换为您需要等待加载的元素 ID
        )

        time.sleep(10)
        # 展开/折叠侧边栏
        driver.find_element(By.CSS_SELECTOR, sidecar_id()).click()
        driver.find_element(By.CSS_SELECTOR, fullscreen_id()).click()
        driver.save_screenshot('2_' + screenshot_name)

        # 菜单 03
        time.sleep(1)
        # 展开/折叠侧边栏
        driver.find_element(By.CSS_SELECTOR, fullscreen_id()).click()  # 取消全屏
        driver.find_element(By.CSS_SELECTOR, sidecar_id()).click()  # 展开侧边栏

        while True:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, item_id(4)).click()  # 点击目标菜单
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.ID, 'DATASHEET_VIEW_CONTAINER_ID'))  # 替换为您需要等待加载的元素 ID
                )
                time.sleep(5)
                break
            except TimeoutException:
                driver.find_element(By.CSS_SELECTOR, item_id(5)).click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, item_id(6)).click()
                time.sleep(2)

        js_height = "return document.body.clientHeight"
        height = driver.execute_script(js_height)

        k = 1
        while True:
            # 滚动到底部，但是不超过 3241
            if k * 1080 < height and k * 1080 < 3241:
                js_move = f"window.scrollTo(0,{k * 1080})"
                driver.execute_script(js_move)
                time.sleep(0.5)
                height = driver.execute_script(js_height)
                k += 1

            else:
                break

        total_height = f"""
        var element = document.getElementsByClassName('style_verticalScrollBarInner__J29XF')[0];
        var heightStyle = window.getComputedStyle(element).getPropertyValue('height');
        return parseFloat(heightStyle);
        """

        height = driver.execute_script(total_height)
        driver.set_window_size(1920, height)

        driver.find_element(By.CSS_SELECTOR, sidecar_id()).click()
        time.sleep(3)
        bytes_content = driver.get_screenshot_as_png()

        with open('3_' + screenshot_name, 'wb') as f:
            f.write(bytes_content)

        return [
            '1_' + screenshot_name,
            '2_' + screenshot_name,
            '3_' + screenshot_name
        ]

    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        driver.quit()


def screenshot_for_url(url: str, screenshot_name: str = 'screenshot.png'):
    options = Options()
    options.add_argument("--headless")  # 指定使用无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速，某些系统/驱动程序可能需要
    options.add_argument("--window-size=1920x1440")  # 设置窗口大小，确保网页元素完全显示
    options.add_argument("--no-sandbox")  # 以最高权限运行
    options.add_argument("--disable-dev-shm-usage")  # 禁用/dev/shm 使用，某些系统可能需要
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-infobars")  # 禁用信息栏

    try:
        driver = webdriver.Chrome(service=Service(
            chromedrvier_path), options=options)

        # 下面是截图
        driver.get(url)
        driver.fullscreen_window()
        driver.save_screenshot(screenshot_name)
        return "screenshot success!"

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return "screenshot failed!"
    finally:
        driver.quit()

