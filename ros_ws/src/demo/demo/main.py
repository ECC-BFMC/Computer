import rclpy
from rclpy.node import Node
from cv_bridge       import CvBridge
import cv2

from std_msgs.msg import Float32, Bool, String, Int8
from sensor_msgs.msg import Image


from functools import partial 

from demo.obj.UI    import UI

class GUI_Demo(Node):   
         
    def __init__(self):
        super().__init__('GUI_Demo')
        
        # To be deleted!
        filename = '/home/bfmccomputer/Documents/11_ECC-BFMC-Computer/src/demo/demo/obj/21-09-17-12-39-53.mp4'
        self.cap         =   cv2.VideoCapture(filename)
        # --------------

        self.timer = self.create_timer(0.01, self.mainLoop)

        self.SetRefSpeedPUB = self.create_publisher(Float32,    '/Vehicle/Output/Speed/Ref',    1)
        self.SetRefSteerPUB = self.create_publisher(Float32,    '/Vehicle/Output/Steer/Ref',    1)
        self.StartEnginePUB = self.create_publisher(Bool,       '/Vehicle/System/Engine/Running',1)
        self.image_publisher = self.create_publisher(Image,     '/Vehicle/Input/Camera/image_raw',1)
        

        subscriberIMUacceleration   = self.create_subscription(String, "/Vehicle/Input/IMU/Acceleration", partial(self.sub_, "IN_IMU_ACC", 1), 1)
        subscriberIMUrotation       = self.create_subscription(String, "/Vehicle/Input/IMU/Rotation", partial(self.sub_, "IN_IMU_ROT"), 2)
        subscriberLOCSYSposiiton    = self.create_subscription(String, "/Vehicle/Input/Locsys/Position", partial(self.sub_, "IN_LOC_POS", 3), 1)
        subscriberBATTERYlevel      = self.create_subscription(Int8, "/Vehicle/System/Battery/Level", partial(self.sub_, "SYS_BAT_LVL", 4), 1)
        subscriberENGINEoperable    = self.create_subscription(Bool, "/Vehicle/System/Engine/Operable", partial(self.sub_, "SYS_EN_OPE", 5), 1)
        subscriberENGINErunning     = self.create_subscription(Bool, "/Vehicle/System/Engine/Running", partial(self.sub_, "SYS_EN_RUN", 6), 1)
        subscriberMOBILEVEHICLEpos  = self.create_subscription(String, "/Vehicle/Input/MobileVehicle/Position", partial(self.sub_, "IN_MOB_VEH", 7), 1)
        subscriberSEMAPHOREone      = self.create_subscription(Int8, "/Vehicle/Input/Semaphore/One", partial(self.sub_, "IN_SEM_1", 8), 1)
        subscriberSEMAPHOREtwo      = self.create_subscription(Int8, "/Vehicle/Input/Semaphore/Two", partial(self.sub_, "IN_SEM_2", 9), 1)
        subscriberSEMAPHOREthree    = self.create_subscription(Int8, "/Vehicle/Input/Semaphore/Three", partial(self.sub_, "IN_SEM_3", 10), 1)
        subscriberSEMAPHOREfour     = self.create_subscription(Int8, "/Vehicle/Input/Semaphore/Four", partial(self.sub_, "IN_SEM_4", 11), 1)
        subscriberCAMERAraw         = self.create_subscription(Image, "/Vehicle/Input/Camera/image_raw", self.camera_callback, 1)

        self.UI = UI(self.sendSpeed, self.sendSteer, self.sendStartEngine)  
        self.bridge = CvBridge()          
    
    def createGUI(self):
        self.UI.create()

    def sendSpeed(self, val):
        var = Float32()
        var.data = float(val)
        self.SetRefSpeedPUB.publish(var)

    def sendSteer(self, val):
        var = Float32()
        var.data = float(val)
        self.SetRefSteerPUB.publish(var)
        print("whyy??")

    def sendStartEngine(self, val):
        var = Bool()
        var.data = val
        self.StartEnginePUB.publish(var)

    def sub_(self, type, id, msg):
        self.UI.modifyTable(type, id, msg.data)    

    def camera_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        self.UI.modifyImage(image)

    def mainLoop(self):
        # To be deleted!
        ret, frame = self.cap.read()
        if ret: 
            imageObject = self.bridge.cv2_to_imgmsg(frame, "bgr8") #BGR because ros2 ImageViewr uses this color order.
            imageObject.header.stamp = self.get_clock().now().to_msg()
            self.image_publisher.publish(imageObject)
        # --------------
        self.UI.update()


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = GUI_Demo()
    minimal_subscriber.createGUI()
    rclpy.spin(minimal_subscriber)


if __name__ == "__main__":
    main()
    