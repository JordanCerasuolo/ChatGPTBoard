# ChatGPTBoard
Python script to use ChatGPT on a raspberry pi 400 whilst emulating a keyboard.

See usage intrustions for more information on what this actually does.


# Requirements
1. Python3 - if you do not have it, install it with ```sudo apt update``` + ```sudo apt install python3```
2. Python3-pip - if you do not have it, install it with ```sudo apt update``` + ```sudo apt install python3-pip```
3. Continue to installation.





# Installation

1. install python console and openai as root and normal user.
```
pip install console
pip install openai
pip install pygame
sudo pip install console
sudo pip install openai
sudo pip install pygame
```
2. install the drivers for the HID interface, and set it to launch at boot: (full guide under references.)
 ```
 echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
 echo "dwc2" | sudo tee -a /etc/modules
 sudo echo "libcomposite" | sudo tee -a /etc/modules
 sudo touch /usr/bin/isticktoit_usb
 sudo chmod +x /usr/bin/isticktoit_usb
 sudo nano /etc/rc.local
 ```
 Add the following before exit 0, and then save and exit nano:
 ```
 /usr/bin/isticktoit_usb # libcomposite configuration
 ```
 ```
 sudo nano /usr/bin/isticktoit_usb
 ```
 paste this into the isticktoit_usb file:
 
 
```
#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Tobias Girstmair" > strings/0x409/manufacturer
echo "iSticktoit.net USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/
# End functions

ls /sys/class/udc > UDC
```

Save and exit this file. To confirm everything worked successfully, reboot the pi and it should be now recognized by a computer if plugged in.


3. download the python script into the home folder of your pi 400

4. edit the variables inside the script to your liking, and change the openai key to your key (line 93/94)

5. add "sudo python3 GPTBoard.py" to the end of your .bashrc in the home directory

6. test



# References - these are important resources that may help, or that I used to make this project:
https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/ - guide to create the HID device

https://pimylifeup.com/raspberry-pi-pip/ - guide to install python-pip

https://www.usb.org/developers/hidpage/Hut1_12v2.pdf - HID Device reference sheet (look on wayback machine to download)





# Usage Instructions:
When the keyboard is plugged in via a usb-c cable to a computer that can deliver 5v, if the cable can deliver power and data, then the computer should recognize the pi400 as a generic USB keyboard. Once this happens, the numlock LED should flash multiple times to signal that the pi has booted (as long as the script was run with root and everything worked)

After the LED has flashed, most keys on the pi400 should work as keyboard keys for the computer it is plugged into, however I have not gotten special characters worrking, or even numbers unfortunately. 

When the zero key is pushed, the numlock LED should turn red for a second. After it turns back off, the keyboard has entered chatGPT mode.

When the LED turns back off, whatever you type on the pi400 will be sent to chatGPT after hitting enter.

Once enter is pushed, the LED should turn back on letting you know it is thinking.

If everything worked and the pi400 has internet/you used a working openai key, the LED should turn back off eventually when it has recieved the response from chatGPT.

Here comes the fun part: When the LED is back off, whatever character that you press, will be turned into the next character that chatGPT returned. This means that you can press any letter, and it will change before being sent to the computer. 

(This is more of a fun and cool-looking way to actually type out the response from chatGPT, however if it is not your cup of tea, you can comment out the section of the python script that says #new typing method, and then uncomment the loop above it)

When everything has been typed out, there should be a  short pause and then the pi400 will return to normal keyboard functionality.



# Things To Add:
1. more functional keys, such as shift and the number row.
2. customizable keybinds
3. possible web interface for configuration




