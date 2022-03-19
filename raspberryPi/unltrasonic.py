# Libraries
import RPi.GPIO as GPIO
import time

from send_request import update_status

bin_name = "BIN_0"

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGERs = [18, 19, 20]
GPIO_ECHOs = [24, 25, 26]

names = ["Can", "PET", "Box"]

moving_avgs = [-1] * 3
smooth_rate = 0.9

# set GPIO direction (IN / OUT)
for trig_pin in GPIO_TRIGGERs:
    GPIO.setup(trig_pin, GPIO.OUT)

for echo_pin in GPIO_ECHOs:
    GPIO.setup(echo_pin, GPIO.IN)


def distance(ind):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERs[ind], True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERs[ind], False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHOs[ind]) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHOs[ind]) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def update_ultrasonic():
    for i in range(3):
        if moving_avgs[i] == -1:
            moving_avgs[i] = distance(i)
        moving_avgs[i] = moving_avgs[i] * smooth_rate + distance(i) * (1 - smooth_rate)

        if moving_avgs[i] < 12:
            print(f"{names[i]} is full")
            update_status(bin_name, f"{names[i]}Full", "true")
        else:
            update_status(bin_name, f"{names[i]}Full", "false")

    time.sleep(1)


if __name__ == "__main__":
    try:
        while True:
            print(moving_avgs)
            update_ultrasonic()

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
