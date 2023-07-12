# BFMC - Computer Project

The project contains all the provided code that will run on the PC, and it's made of 4 parts:
- Demo: The official RPi image starts automatically a communication. You will have to find out the IP of the RPi and insert it into threadRemoteHandlerPC, line 44, and then start the demo.py. From here you can see the messages that the car receives from the Nucleo, the images and, if the simulated devices are running, the messages that it gets from them.
- Dashboard: A monitoring application for all the systems from the car. Once you start developing you can debug in real-time the info in this application.
- carsAndSemaphoresStreamSIM: The simulated stream. Sends random, simulated data about the semaphores and the cars on the track, just as our servers at the Bosch location.
- trafficCommunicationServer: The simulated server of the challenge. The car can get from this server the IP of the localization device and send to it information during the run (Speed, position, rotation and encountered obstacles.)

## The documentation is available in more details here:
[Documentation](https://boschfuturemobility.com/brain/)
