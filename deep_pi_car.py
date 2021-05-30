import logging
import picar
import cv2
import datetime


class DeepPiCar(object):
    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 320

    def __init__(self):
        """
        set up my camera and wheels
        """
        logging.info("Creaing a Car")
        picar.setup()

        logging.debug("set up camera")
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)

        self.pan_servo = picar.Servo.Servo(1, bus_number=1)
        self.pan_servo.offset = 10
        self.pan_servo.write(90)

        self.tilt_servo = picar.Servo.Servo(2, bus_number=1)
        self.pan_servo.offset = 0
        self.pan_servo.write(90)

        logging.debug("Set up rear wheels")
        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.speed = 0

        logging.debug("Set up front wheels")
        self.front_wheels = picar.front_wheels.Front_Wheels()
        self.front_wheels.turn(90)

        logging.info("Finished setting up the Car")

    def __enter__(self):
        """Entering a with statement"""
        return self

    def __exit__(self, _type, value, traceback):
        """Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error("Exiting with statement with exception %s" % traceback)

    def drive(self, speed):
        logging.info("Starting to drive at speed %s..." % speed)

        self.back_wheels.speed = speed
        while self.camera.isOpened():

            self.front_wheels.turn(120)
            self.back_wheels.backward()
            _, image_lane = self.camera.read()
            cv2.imshow("Lane Lines", image_lane)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.back_wheels.stop()
                self.camera.release()
                cv2.destroyAllWindows()
                break


def main():
    with DeepPiCar() as car:
        car.drive(20)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)-5s:%(asctime)s: %(message)s"
    )

    main()
