from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

# 打开登录页面
print("Start open.")
driver.get('https://sendeltastudent.schoolis.cn/')
print("Finish open.")

UserName = "tangzijia"
PassWord = "Aa&814777"

# 定位用户名和密码输入框，并输入用户名和密码
input_xpath = '//*[@id="/html/body/div/login-layout/div/div/login-body/div/div/div/login-enter-box/div/div/div[2]/div[2]/div[1]/input"]'
wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.visibility_of_element_located((By.XPATH, input_xpath)))
username_input.click()
username_input.send_keys('tangzijia')

input_xpath = '//*[@id="/html/body/div/login-layout/div/div/login-body/div/div/div/login-enter-box/div/div/div[2]/div[2]/div[2]/input"]'
password_input = driver.find_element(By.XPATH,input_xpath)
password_input.click()
password_input.send_keys('your_password')

# 提交登录表单
password_input.send_keys(Keys.RETURN)

x = input()

# url = 'https://sendeltastudent.schoolis.cn/'
# /html/body/div/login-layout/div/div/login-body/div/div/div/login-enter-box/div/div/div[2]/div[2]/div[1]/input
# /html/body/div/login-layout/div/div/login-body/div/div/div/login-enter-box/div/div/div[2]/div[2]/div[2]/input
# document.querySelector("body > div > login-layout > div > div > login-body > div > div > div > login-enter-box > div > div > div.fe-components-stu-business-login-enter-box-__loginInformation--W2yiibeHcVKj_lJeq1rW_ > div.fe-components-stu-business-login-enter-box-__accountContainer--22PmjI_OEsahZLiUEgL4zr > div:nth-child(1)")