from machine import Pin
from umqtt import MQTTClient
import pycom, machine
import uos
import time
import boot

#try connect to broker, wait if cant
def tryConnect():
	try:
		mqtt.connect()
		return True
	except:
		#time.sleep(2)
		return False

def reset():
	with open('count.txt','w') as f:
		f.write('0')
	global count
	count = 0
	print('reset')

def msg(topic,msg):
	print(msg)
	if msg.decode() == 'reset':
		reset()
        
subscribed = False
pycom.heartbeat(False)
wlan=WLAN(mode=WLAN.STA)
#Set pin G23 as input with resistor down
P2 = Pin('P2', mode=Pin.IN, pull=Pin.PULL_DOWN)
button=Pin("G17",Pin.IN, pull=Pin.PULL_UP)
#id of client and ip of Pi wifi
mqtt = MQTTClient('LoPy','192.168.5.1')
mqtt.set_callback(msg)
if not wlan.isconnected():
	boot.wlanConnect()
isConnected = tryConnect()


try:
	#uos.stat throws error if count.txt doesn't exist
	uos.stat('count.txt')
	#tries to read count of previous run, if can't thne count =  0
	with open('count.txt','r') as f:
		try:
			count = int(f.read())
		except:
			count = 0
			f.close()
	#wipe count.txt and write count of old run
	with open('count.txt','w') as f:
		f.write(str(count))
#runs if no previous count.txt
except:
	#create count.txt
	with open('count.txt','x') as f:
		f.close()
	#write count as 0
	with open('count.txt','w') as f:
		f.write('0')
		count = 0


while True:
		if not subscribed:
				try:
					mqtt.subscribe('test/message')
					subscribed = True
				except:
					subscribed = False
		mqtt.check_msg()
		if not wlan.isconnected():
			boot.wlanConnect()
		#if not connected to broker try again, if cant wait 2 seconds
		if not isConnected:
			isConnected = tryConnect()
		if button()==0 & isConnected:
			reset()
		#if input from radar and is connected to broker
		if P2()==1 & isConnected & subscribed:
			count+=1
			#publish count
			mqtt.publish('test/message',str(count))
			f = open('count.txt','w')
			f.write(str(count))
			f.close()
			time.sleep(2.1)
