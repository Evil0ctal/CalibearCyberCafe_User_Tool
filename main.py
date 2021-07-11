# -*- coding: utf-8 -*-
# @Author  : Evil0ctal
# @Time    : 2021/07/10
# @Function:
# Ask user input a number then help them finish registration or reset password

import requests
import json
import re


def check(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not regex.match(email):
        return "Invalid Email"
    else:
        return "Valid Email"


def registration(email):
    if check(email) == "Valid Email":
        try:
            registration_url = "https://calibear.bebooking.enes.tech/user/"
            registration_payload = {"login": email}
            registration_response = requests.post(registration_url, data=json.dumps(registration_payload),
                                                  headers=headers).text
            response_id = json.loads(registration_response)
            global user_id
            user_id = int(response_id['id'])
            print("The email you input is: " + email + "\nYour user ID is: " + str(user_id))
        except:
            print("Something wrong with registration,please contact our staff.")
    else:
        print("Please enter an valid email address.")
        return -1


def activation(activation_code):
    try:
        activation_payload = {"activation_code": str(activation_code)}
        activation_url = "https://calibear.bebooking.enes.tech/user/" + str(user_id) + "/activate/"
        activation_response = requests.post(activation_url, data=json.dumps(activation_payload), headers=headers).text
        activation_result = json.loads(activation_response)
        if "detail" in activation_result:
            print(str(activation_result['detail']) + ",please enter a correct code.")
        else:
            print(
                "Thanks for register at Calibear!\nYour account information and password had been send to your email!")
    except:
        print("Something wrong with activation,please contact our staff.")


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
                    print("Sorry,User with such login does not exists")
                    return -1
            else:
                print(
                    "You received confirmation code on your e-mail.\nAfter successful confirmation, you will receive new password on e-mail.")
        except:
            print("Something wrong with reset password,please contact our staff.")
    else:
        print("Please enter an valid email address.")
        return -1


def reset_password_code_confirm(email, reset_password_code):
    if reset_password_code.isdigit():
        try:
            reset_password_code_payload = {"login": email, "code": reset_password_code}
            reset_password_code_url = "https://calibear.bebooking.enes.tech/user/reset_password/"
            reset_password_code_response = requests.post(reset_password_code_url,
                                                         data=json.dumps(reset_password_code_payload),
                                                         headers=headers).text
            if "Invalid user reset password code" in reset_password_code_response:
                print("Invalid user reset password code!")
            else:
                print("Thank you,a new password had been sent to your email!")
                print('')
        except:
            print("Sorry,something went wrong while we try to reset your password,please contact our staff.")
    else:
        print("Please enter the numbers only!")


while True:
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://calibear.booking.enes.tech/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    try:
        options = input(
            "Hi,welcome to Calibear!\nPlease select the command you want to execute.\nEnter '1' to make a registration,enter '2' to reset your password.\nPlease enter a number: ")
        if options.isdigit():
            options = int(options)
            if options == 1:
                try:
                    email = str(input("Please Input your Email: "))
                    if registration(email) != -1:
                        activation_code = input(
                            'An activation code had been sent to your Email!\nPlease input the activation code here: ')
                        if activation_code.isdigit():
                            activation(int(activation_code))
                        else:
                            print("Sorry,the activation code must be an number.")
                except:
                    pass
            elif options == 2:
                try:
                    email = str(input("Please Input your Email: "))
                    if reset_password(email) != -1:
                        reset_password_code = input("please input your confirmation code here: ")
                        reset_password_code_confirm(email, reset_password_code)
                except:
                    pass
            else:
                print("Sorry,there is no that option,please select between '1' or '2'")
    except:
        print("Sorry,something went wrong with program,please contact our staff.")
