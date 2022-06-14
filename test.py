from selenium import webdriver

browser= webdriver.Firefox()

browser.get('https://www.nakedtrader.co.uk/trades/agree.htm?agree=1')

new_releases= browser.find_element_by_link_text('.agree.htm?agree=1')

new_releases.click()
