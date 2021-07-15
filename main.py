# -*- coding: utf-8 -*-
# @Author  : Evil0ctal
# @Time    : 2021/07/10
# @Function:
# After obtaining the parameters entered by the guests at the front desk, verify it, and submit a POST request to the Senet server to complete the account registration, reset the password, and print the result to the console without an API key.
# 获取前台客人输入的参数后进行校验，无误后向Senet服务器提交POST请求完成注册账户，重置密码，并将结果打印至控制台，无需API key。

import qrcode_terminal
import requests
import hashlib
import json
import sys
import re
import os


# 正则检查用户输入是否为Email格式
def check(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not regex.match(email):
        return "Invalid Email"
    else:
        return "Valid Email"

# 清空控制台残留消息
def clear():
    f_handler = open('out.log', 'w')
    oldstdout = sys.stdout
    sys.stdout = f_handler
    os.system('cls')
    sys.stdout = oldstdout

# 生成MD5校验管理员密码
def genearteMD5(str):
    exit_code = hashlib.md5()
    exit_code.update(str.encode(encoding='utf-8'))
    exit_code_md5 = exit_code.hexdigest()
    return exit_code_md5

# 提交注册POST请求
def registration(email):
    if check(email) == "Valid Email":
        try:
            registration_url = "https://calibear.bebooking.enes.tech/user/"
            registration_payload = {"login": email}
            registration_response = requests.post(registration_url, data=json.dumps(registration_payload),headers=headers).text
            response_id = json.loads(registration_response)
            if response_id['login'] != email:
                clear()
                print('')
                print("[Error]")
                print("User with such email already exists!")
                print("Please try another email or reset your password!")
                return -1
            else:
                global user_id
                user_id = int(response_id['id'])
                clear()
                print('')
                print("[Account Activation]")
                print("The email you input is: " + email)
        except:
            clear()
            print('')
            print("[Error]")
            print("Something wrong with registration,please contact our staff.")
    else:
        clear()
        print('')
        print("[Error]")
        print("Please enter an valid email address.")
        return -1

# 提交激活POST请求
def activation(activation_code):
    try:
        activation_payload = {"activation_code": str(activation_code)}
        activation_url = "https://calibear.bebooking.enes.tech/user/" + str(user_id) + "/activate/"
        activation_response = requests.post(activation_url,data=json.dumps(activation_payload),headers=headers).text
        activation_result = json.loads(activation_response)
        if "detail" in activation_result:
            clear()
            print('')
            print("[Error]")
            print("Invalid user validation code!")
            print("please enter the correct code.")
        else:
            clear()
            # 干，QRcode太大了，有时候不能正常显示
            print("[Order Online QR-code]")
            qrcode_terminal.draw("https://calibearcybercafe.applova.menu/")
            print('')
            print("[Registration Complete]")
            print("Thanks for register at Calibear!")
            print("Your account information and password had been sent to your email!")
            print("Please use them login to client PC")
            print('')
            print("[Top Up Balance]")
            print("Go to front desk talk our staff.")
            print("Visit our online store,place order and leave your info with note.")
            print("Online Store Link: https://calibearcybercafe.applova.menu")
            print('')

    except:
        clear()
        print('')
        print("[Error]")
        print("Something wrong with activation,please contact our staff.")

# 提交重置密码POST请求
def reset_password(email):
    if check(email) == "Valid Email":
        try:
            reset_password_url = "https://calibear.bebooking.enes.tech/user/send_reset_password_code/"
            reset_password_payload = {"login": email}
            reset_password_response = requests.post(reset_password_url, data=json.dumps(reset_password_payload),
                                                    headers=headers).text
            if reset_password_response != '':
                reset_password_result = json.loads(reset_password_response)
                if reset_password_result['code'] == -2:
                    clear()
                    print('')
                    print("[Error]")
                    print("Sorry,User with such login does not exists")
                    return -1
            else:
                clear()
                print('')
                print("You received a confirmation code on your Email.")
                print("After successful confirmation, you will receive new password on Email.")
        except:
            clear()
            print('')
            print("[Error]")
            print("Something wrong with reset password,please contact our staff.")
    else:
        clear()
        print('')
        print("[Error]")
        print("Please enter an valid email address.")
        return -1

# 提交重置密码验证码POST请求
def reset_password_code_confirm(email,reset_password_code):
    if reset_password_code.isdigit():
        try:
            reset_password_code_payload = {"login": email, "code": reset_password_code}
            reset_password_code_url = "https://calibear.bebooking.enes.tech/user/reset_password/"
            reset_password_code_response = requests.post(reset_password_code_url,data=json.dumps(reset_password_code_payload),headers=headers).text
            if "Invalid user reset password code" in reset_password_code_response:
                clear()
                print('')
                print("[Error]")
                print("Invalid user reset password code!")
            else:
                clear()
                print('')
                print("[Password Reset Complete]")
                print("Thank you,a new password had been sent to your email!")
        except:
            clear()
            print('')
            print("[Error]")
            print("Sorry,something went wrong while we try to reset your password,please contact our staff.")
    else:
        clear()
        print('')
        print("[Error]")
        print("Please enter the numbers only!")

# 核心代码 估值2亿 ：）
while True:
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://calibear.booking.enes.tech/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    try:
        # 可以写入文件再读取，但是我懒，一个变量解决。
        exit_md5 = '47c440a3cfbed2f49c00ad6c1103d487'
        print('')
        print("##########################################")
        print("# [CalibearCyberCafe User Tool]          #")
        print("# Enter '1' to make a registration.      #")
        print("# Enter '2' to reset your password.      #")
        print("# Press 'Enter key' to skip.             #")
        print("# Select option again after skip.        #")
        print("##########################################")
        options = input("Please enter a number here: ")
        if genearteMD5(options) == exit_md5:
            print("The Admin Password Match,Break now...")
            print("To rerun: type 'python main.py'")
            break
        elif options.isdigit():
            options = int(options)
            if options == 1:
                try:
                    print('')
                    print("[Account Registration]")
                    email = str(input("Please enter your Email here: "))
                    if registration(email) != -1:
                        print("An activation code had been sent to your Email!")
                        print("If you did not receive the email, please check your spam.")
                        activation_code = input('Please input the activation code here: ')
                        if activation_code.isdigit():
                            activation(int(activation_code))
                        else:
                            clear()
                            print('')
                            print("[Error]")
                            print("Sorry,the activation code must be an number.")
                except:
                    pass
            elif options == 2:
                try:
                    clear()
                    print('')
                    print("[Reset Password]")
                    email = str(input("Please input your Email here: "))
                    if reset_password(email) != -1:
                        reset_password_code = input("please input your confirmation code here: ")
                        reset_password_code_confirm(email, reset_password_code)
                except:
                    pass
            # 不会真的有人选3吧，不会吧不会吧
            elif options == 3:
                clear()
                print('')
                print("# Author                               ")
                print("# WeChat : Evil0ctal                   ")
                print("# Time   : 2021/07/10                  ")
                print("# GitHub : https://github.com/Evil0ctal")
                print('')
            else:
                clear()
                print('')
                print("[Error]")
                print("Sorry,there is no that option,please select between '1' or '2'")
        else:
            clear()
            print('')
            print("[Error]")
            print("Sorry,there is no that option,please select between '1' or '2'")

    except:
        clear()
        print('')
        print("[Error]")
        print("Sorry,something went wrong with program,please contact our staff.")
