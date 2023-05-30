#!/usr/bin/env python3
NULL_CHAR = chr(0)

import pygame
import time
from codes import *
from time import sleep
import openai
import console
from console.utils import wait_key
import os
import fcntl

def write_report(report): #setup the keyboard emulation
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())



# set variables for leds
KDSETLED = 0x4B32
NUM_LED  = 0x02

console_fd = os.open('/dev/console', os.O_NOCTTY)

pygame.init() # initialize pygame



for x in range(5):
    # blink the numlock LED a few times to show the script is running/pi has started completeley if autostart
    fcntl.ioctl(console_fd, KDSETLED, NUM_LED) # turn on numlock LED for status
    sleep(0.1)
    fcntl.ioctl(console_fd, KDSETLED, 0) # turn off numlock LED for status
    sleep(0.1)

def typeKey(keyNumber, caps): # define function to type a key with an input of the key number from the USB HID documentation
    if keyNumber == 34:
        write_report(caps+NULL_CHAR+chr(42)+NULL_CHAR*5)
        return
    
    if keyNumber > 0:
        write_report(caps+NULL_CHAR+chr(keyNumber)+NULL_CHAR*5) # type the character based on the number/letter
    else:
        try:
            write_report(caps+NULL_CHAR+chr(specialChars[f"{keyNumber}"])+NULL_CHAR*5)
        except:
            return
    


def chatGPT():
    sleep(0.1) # temporary wait time
    fcntl.ioctl(console_fd, KDSETLED, NUM_LED) # turn on numlock LED for status
    sleep(1)
    fcntl.ioctl(console_fd, KDSETLED, 0)
    userPrompt = input("Enter the prompt for ChatGPT: ") # get the input from the user for the ChatGPT prompt to be typed

    sleep(0.1) # temporary wait time

    fcntl.ioctl(console_fd, KDSETLED, NUM_LED)
    openai.api_key = "INSERT YOUR API KEY HERE" # input your openai API key here
    model_engine = "gpt-3.5-turbo" # setting up the model to be used

    prompt = [{"role": "user", "content": userPrompt}] # create the prompt to be given from what the user inputted


    completion = openai.ChatCompletion.create( # send the request to the openai API
        model=model_engine,
       messages=prompt,
        max_tokens=1024,
       n=1,
       stop=None,
       temperature=0.5,
    )

    response = completion.choices[0].message.content # store the response from ChatGPT

    print(response) # print the response gotten

    characterList = ([*response]) # turn the response into individual characters

    #for x in characterList: # for each character of ChatGPT's response:
    #    numberToType = ord(x) - 93 # turn the character into a number starting from 4 to align with the USB HID documentation
    #    typeKey(numberToType) # run the aforementioned function
    #    sleep(0.001)

    # new typing method:
    fcntl.ioctl(console_fd, KDSETLED, 0)
    for x in range(len(characterList)):
        #print(x)
        wait_key()
        numberToType = ord(characterList[x]) - 93
        print(numberToType)
        if x.isupper():
            caps = chr(32)
        else:
            caps = NULL_CHAR
        typeKey(numberToType, caps)
        write_report(NULL_CHAR*8)



    # Release all keys
    write_report(NULL_CHAR*8) # stop pressing any special characters
    sleep(1)
    fcntl.ioctl(console_fd, KDSETLED, 0) # turn off numlock LED for status
    keyboardEmu()






# main typing loop

def keyboardEmu():
    typedKey = wait_key()
    if typedKey == '0':
        print("Gpting")
        sleep(0.1)
        chatGPT()
        
    else:
        tempNum = ord(typedKey) - 93
        print(tempNum)
        caps = NULL_CHAR
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LSHIFT]:
            caps = chr(32)
        typeKey(tempNum, caps)
        write_report(NULL_CHAR*8) # stop pressing
        keyboardEmu()


keyboardEmu()




