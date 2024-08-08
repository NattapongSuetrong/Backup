from serial.tools import list_ports
import pydobot 
import pygame
import gtts


available_port = list_ports.comports()
print(f'available port:{[x.device for x in available_port]}')
port = available_port[0].device

device = pydobot.Dobot(port=port, verbose=True)


r=0
(x_home, y_home, z_home) = 239,0,130
(x_pointA, y_pointA, z_pointA) = 290,-16.5,-37.2
(x_pointB, y_pointB, z_pointB) = 236.5,112.9,-13.1

device.move_to(x_home, y_home, z_home, r , wait=True)

def a_to_b():
	text = "A to B"
	tts = gtts.gTTS(text, lang='th')
	tts.save('output.mp3')
	pygame.mixer.init()
	pygame.mixer.music.load('output.mp3')
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue
	pygame.mixer.quit()
	device.move_to(x_pointA, y_pointA, 130, r , wait=True)
	device.move_to(x_pointA, y_pointA, z_pointA, r , wait=True)
	device.suck(True)
	device.move_to(x_pointA, y_pointA, 130, r , wait=True)
	device.move_to(x_pointB, y_pointB, 130, r , wait=True)
	device.move_to(x_pointB, y_pointB, z_pointB, r , wait=True)
	device.suck(False)
	device.move_to(x_home, y_home, 130, r , wait=True)

def b_to_a() :
	text = "B to A"
	tts = gtts.gTTS(text,lang='th')
	tts.save('output.mp3')
	pygame.mixer.init()
	pygame.mixer.music.load('output.mp3')
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue
	pygame.mixer.quit()
	device.move_to(x_pointB, y_pointB, 130, r , wait=True)
	device.move_to(x_pointB, y_pointB, z_pointB, r , wait=True)
	device.suck(True)
	device.move_to(x_pointB, y_pointB, 130, r , wait=True)
	device.move_to(x_pointA, y_pointA, 130, r , wait=True)
	device.move_to(x_pointA, y_pointA, z_pointA, r , wait=True)
	device.suck(False)
	device.move_to(x_home, y_home, 130, r , wait=True)

for i in range(3):
	a_to_b()
	

	
