# This is will hold all of the functions we should need for basic movement. But will definitely need modification and
# testing. I started by copying the imports from the example file move.py as pycharm doesnt seem to recognize it as a
# valid import.
import sys
sys.path.append(r'/opt/ezblock')
from ezblock import __reset_mcu__
import time
__reset_mcu__()
time.sleep(0.01)

from picarx import Picarx


dir_servo_angle_calibration(0)
def forever():
  forward(50)
  delay(1000)
  backward(50)
  delay(1000)
  forward(50)
  set_dir_servo_angle((-30))
  delay(1000)
  forward(50)
  set_dir_servo_angle(30)
  delay(1000)
  set_dir_servo_angle(0)
  stop()
  delay(2000)

if __name__ == "__main__":
    while True:
        forever()