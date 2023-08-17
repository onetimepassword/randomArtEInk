# randomArtEInk
## setup
raspberry pi, [2.7inch e-Paper HAT](https://www.waveshare.com/2.7inch-e-paper-hat.htm)

## install
1. install the Python libraries. 
    - SPI library of Python
    - PIL (Python Imaging Library) library
    - RPi (Raspberry Pi IO Library) library
2. change the current directory to where the demo files located. 
3. mkdir venv 
4. source venv/bin/activate

    https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

5. pip install missing libraries 
6. run the demo with:

    sudo python main.py

## commands
--word "text to display"

###  buttons
|button|action|
| -- | -- |
|key1 |reset clear|
|key2 |reset dark|
|key3 |date time|
|key4 |title|
