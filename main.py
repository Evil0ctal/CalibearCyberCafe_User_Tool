import requests
import json
import re

def check(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not regex.match(email):
        return ("Invalid Email")
    else:
        return ("Valid Email")

def registration(email):
    if check(email) == "Valid Email":
        try:
            registration_url = "https://calibear.bebooking.enes.tech/user/"
            registration_payload = {"login": email}
            registration_response = requests.post(registration_url, data=json.dumps(registration_payload),headers=headers).text
            response_id = json.loads(registration_response)
            user_id = int(response_id['id'])
            return user_id
        except:
            print("Something wrong with registration,please contact our staff.")
    else:
        print("Please enter an valid email address.")
        return -1

def activation(activation_code):
    try:
        activation_payload = {"activation_code": str(activation_code)}
        activation_url = "https://calibear.bebooking.enes.tech/user/" + str(registration(email)) + "/activate/"
        activation_response = requests.post(activation_url, data=json.dumps(activation_payload), headers=headers).text
        activation_result = json.loads(activation_response)
        if "detail" in activation_result:
            print(str(activation_result['detail']))
        else:
            print("Thanks for register at Calibear!\nYour account information and password had been send to your email!")
    except:
        print("Something wrong with activation,please contact our staff.")

while True:
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Referer": "https://calibear.booking.enes.tech/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    try:
        email = str(input("Please Input your Email: "))
        if registration(email) != -1:
            print("The email you input is: " + email + "\nYour user ID is: " + str(registration(email)))
            activation_code = int(input("An activation code had been sent to your Email!\nPlease input the activation code here: "))
            activation(activation_code)
    except:
        print("Something wrong this program,please contact our staff.")
