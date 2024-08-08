import gpiozero as GPIO
import time
#from detectionV3 import ObjectCounter


PUMP_PIN = 23 
led1 = GPIO.LED(27)
led2 = GPIO.LED(17)

relay = GPIO.OutputDevice(PUMP_PIN, active_high=False, initial_value=False)

def Start():
    relay.on()  # เปิดปั๊มน้ำ

def Stop():
    relay.off()  # ปิดปั๊มน้ำ
    
def lightStart():
    led1.on()
    led2.on()

def lightStop():
    led1.off()
    led2.off()

if __name__ == "__main__":
    video_path = 0  # ถ้าใช้กล้องเว็บแคมเป็น input
    output_path = "object_counting_output.avi"
    Start()
    model_count = ObjectCounter(video_path, output_path)
    model_count.process_video()
