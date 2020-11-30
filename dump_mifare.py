from time import sleep

import RPi.GPIO as GPIO

import pn532.pn532 as nfc
from pn532 import *

pn532 = PN532_I2C(debug = False, reset = 20, req = 16)

# Tell RPi that we're using GPIO board
GPIO.setmode(GPIO.BCM)


# The GPIO pin used for LED light
GPIO.setup(19, GPIO.OUT)

# The GPIO pin used for LED light
GPIO.setup(26, GPIO.OUT)
GPIO.output(19, GPIO.LOW)	
GPIO.output(26, GPIO.LOW)	

# Get firmware data
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Key number
key_number = nfc.MIFARE_CMD_AUTH_A

# Authentication Key
auth_key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
key = auth_key

print('Waiting for RFID/NFC card to read from!')

while True:
	# Check if a card is available to read
	uid = pn532.read_passive_target(timeout=0.5)

	# Try again if no card is available.
	if uid is not None:
		print('Found card with UID:', [hex(i) for i in uid])
		break


hatz = []
hatzCorect = ['E5 01 54 23 93 08 04 00 62 63 64 65 66 67 68 69', '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', '00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF', '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', '00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F', '00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF']

# Go through the first 2 sectors (each having 4 blocks)
# To go through all 16 sectors (each having 4 blocks) replace 8 with 64
for i in range(8):
	try:
		block_number = i

		# Authenticate the block using the key
		pn532.mifare_classic_authenticate_block(uid, block_number, key_number, key)

		# Read block's data
		block_data = pn532.mifare_classic_read_block(block_number)

		# Clean each block of data
		data = ' '.join(['%02X' % x for x in pn532.mifare_classic_read_block(block_number)])

		print(i)
		hatz.append(data)
	except nfc.PN532Error as e:
		print(e.errmsg)
		break

if hatz == hatzCorect:
	GPIO.output(26, GPIO.HIGH)	
else:
	GPIO.output(19, GPIO.HIGH)

print(hatz)

sleep(3)
GPIO.cleanup()
