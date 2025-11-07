# -*- coding: utf-8 -*-
import multiprocessing
import traceback
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService

consent_button_xpath_homepage = "//input[@type='submit' and @value='I agree']"
video_links_class_name = "yt-simple-endpoint.ytd-thumbnail"
consent_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
ads_button_selectors = [".ytp-skip-ad button"]
mute_button_class = "ytp-mute-button"
replay_xpath = '//*[@title="Replay"]'

start_time = int(time.time())


def play():
    homepage = "https://www.youtube.com/watch?v=PdzOkN9_F9A"
    print(f"RUN: {start_time} | {homepage}")

    driver = None
    try:
        # Initialize Firefox
        srv = FirefoxService(executable_path=os.path.join("driver", "geckodriver"))
        opt = webdriver.FirefoxOptions()
        opt.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        )
        opt.set_preference("layers.acceleration.disabled", True)
        opt.set_preference("gfx.canvas.azure.accelerated", False)
        opt.set_preference("dom.webdriver.enabled", False)
        opt.set_preference("useAutomationExtension", False)
        opt.set_preference("security.mixed_content.block_active_content", False)
        opt.set_preference("security.mixed_content.block_display_content", False)

        driver = webdriver.Firefox(service=srv, options=opt)
        driver.maximize_window()
        driver.get(homepage)

        # Handle cookie consent
        try:
            consent_overlay = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "dialog"))
            )
            time.sleep(2)
            consent_buttons = consent_overlay.find_elements(By.CSS_SELECTOR, ".eom-buttons button.yt-spec-button-shape-next")
            if len(consent_buttons) > 1:
                accept_all_button = consent_buttons[1]
                accept_all_button.click()
                print(f"RUN: {start_time} | Accepted cookies")
        except Exception:
            print(f"RUN: {start_time} | Cookie modal missing")

        # Wait for video metadata and player
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.ytd-watch-metadata"))
        )
        print(f"RUN: {start_time} | ts {int(time.time())} Video should start shortly")

        movie_player = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        print(f"RUN {start_time} -> YouTube player loaded")

        # Hover and right-click
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()
        ActionChains(driver).context_click(movie_player).perform()

        time.sleep(2)

    except Exception as e:
        print(f"RUN {start_time} -> Error: {traceback.format_exc()}")

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

    return True


if __name__ == "__main__":
    retry = 0
    while retry < 5:
        try:
            play()
            break
        except Exception as e:
            print(
                f"RUN: {start_time} | ts {int(time.time())} Exception outside video playing, retry {retry} {traceback.format_exc()}"
            )

        retry += 1
        time.sleep(5)
