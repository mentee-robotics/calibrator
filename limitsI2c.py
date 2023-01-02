
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
from threading import Thread
import time  


class limitsI2c:
    
    def __init__(self):
        # rospy.init_node('talker', anonymous=True)
        # self.publisher = rospy.Publisher('/watchdog/limit', String, queue_size=10)
        self.left_i2c_bus=(busio.I2C(board.SCL, board.SDA))
        self.right_i2c_bus = (busio.I2C(board.SCL, board.SDA))
        self.left_mcp = MCP23017(self.left_i2c_bus, address=0x21)
        self.right_mcp = MCP23017(self.right_i2c_bus, address=0x20)
        
        # # # # # # # # # # # # # mcp configs # # # # # # # # # 
        
        self.left_dofs = []
        self.right_dofs = []
        
        self.right_joints = {5: "ankle_pitch" , 4: "knee" ,3: "ankle_roll" ,1: "hip_pitch" ,2: "hip_roll" ,0: "hip_yaw" }
        self.left_joints = {5: "knee" , 4: "ankle_roll" ,3: "hip_roll" ,2: "hip_pitch" ,1: "hip_yaw" ,0: "ankle_pitch" }
        
        self.right_last_state = { "knee": True ,  "ankle_pitch": True , "ankle_roll" : True, "hip_pitch" : True, "hip_roll" : True, "hip_yaw" : True}
        self.left_last_state = { "knee": True ,  "ankle_pitch": True , "ankle_roll" : True, "hip_pitch" : True, "hip_roll" : True, "hip_yaw" : True}
        self.limits = { "left_knee": True ,  "left_ankle_pitch": True , "left_ankle_roll" : True, "left_hip_pitch" : True, "left_hip_roll" : True, "left_hip_yaw" : True, 
                       "right_knee": True ,  "right_ankle_pitch": True , "right_ankle_roll" : True, "right_hip_pitch" : True, "right_hip_roll" : True, "right_hip_yaw" : True}
        self.left_buttons = []
        self.right_buttons = []

        self.mcp_bringup()
        
        self.read_limits_thread =Thread(target=self.read_limits)
        self.read_limits_thread.start()
        
# # # # # # # # # # # # # run # # # # # # # # 

    def mcp_bringup(self):  #  configure the pins on the board as INPUT PULLUP
        for left_pin in range(0, 6):
            self.left_buttons.append(self.left_mcp.get_pin(left_pin)) #defines the mcp pins (A0 is 0, A1 is 1 and so on)

        for right_pin in range(0, 6):
            self.right_buttons.append(self.right_mcp.get_pin(right_pin))

        for pin in self.left_buttons:
            pin.direction = Direction.INPUT  # defines the pins as input pins = recieves data
            pin.pull = Pull.UP  # enabeling pull up resitor on selected pins

        for pin in self.right_buttons:
            pin.direction = Direction.INPUT
            pin.pull = Pull.UP
        
        
    def read_limits(self):
        while True:

            for left_button in self.left_buttons:
                
                key =  self.left_buttons.index(left_button)
                joint =  self.left_joints.get(key)
                current_value = left_button.value
                last_state = self.left_last_state.get(joint)   # reads the last state of the inspected pin from the last state dictionary

                if (current_value != last_state):  
                    self.left_last_state[joint] = current_value # updates the last state (true/false) of the pin in the dictionary
                    self.limits["left_"+joint] = current_value
                    print(self.limits)
                    if (current_value == False):
                        # self.publisher.publish(f"left_{joint}_limit")
                        
                        print(f"left_{joint}_limit")
                    else:
                        # self.publisher.publish(f"left_{joint}_ok")
                        print(f"left_{joint}_ok")
                    time.sleep(0.1)

            
            for right_button in self.right_buttons:
                
                key =  self.right_buttons.index(right_button)
                joint =  self.right_joints.get(key)
                current_value = right_button.value
                last_state = self.right_last_state.get(joint)   # reads the last state of the inspected pin from the last state dictionary

                if (current_value != last_state):  
                    self.right_last_state[joint] = current_value # updates the last state (true/false) of the pin in the dictionary
                    self.limits["right_"+joint] = current_value
                    print(self.limits)
                    if (current_value == False):
                        # self.publisher.publish(f"right_{joint}_limit")
                        print(f"right_{joint}_limit")
                    else:
                        # self.publisher.publish(f"right_{joint}_ok")
                        print(f"right_{joint}_ok")        
                    time.sleep(0.1)