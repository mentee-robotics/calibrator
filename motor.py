import pyCandle
import time, math  
from dataclasses import dataclass
import numpy as np

@dataclass
class MotorData:
    actual_position: float = None
    act_vel: float = None
    act_effort: float = None
    t_stamp: float = None


class Motor:
    def __init__(self, cfg, name, motor_id, mot_index, limits, candle):
        self.candle = candle
        self.limits = limits  

        self.name = name
        self.motor_id = motor_id
        self.motor_params = cfg.robot_params.joints_params[name]
        self.position_pid_params = cfg.robot_params.position_pid_params[name]
        self.joints_params = cfg.robot_params.joints_params[name]
        self.calibration_gesture_params = cfg.robot_params.calibration_gesture_params
        self.impedance_params = cfg.robot_params.impedance_params[name]
        self.init_pos = cfg.robot_params.default_joint_angles_init[name]
        # Motor's params
        self.max_pos = self.motor_params["max_position"]
        self.min_pos = self.motor_params["min_position"]
        self.calibration_delta = self.calibration_gesture_params["delta_pos"]
        self.index = mot_index
        self.actual_data = MotorData()
        self.in_allowed_range = True
        self.locked = True
        self.add_new_motor()
          
            
    def add_new_motor(self):
        self.candle.addMd80(self.motor_id)

    def publish_enable_cmd(self):
        self.candle.controlMd80Enable(self.motor_id, True)
        self.candle.controlMd80Enable(self.motor_id, True)

    def publish_disabled_cmd(self):
        self.candle.controlMd80Enable(self.motor_id, False)

    def publish_zero_cmd(self):
        self.candle.controlMd80SetEncoderZero(self.motor_id)  
    
    def stay_in_pos(self):
        self.update_motor_actual_metadata()
        time.sleep(0.01)
        while self.locked:
            self.candle.md80s[self.index].setTargetPosition(self.actual_data.actual_position)
            time.sleep(0.1)
    
    def move_motor(self):
        t = 0.0
        dt = 0.2
        for i in range(1000):
            t = t  + dt
            self.candle.md80s[self.index].setTargetPosition(math.sin(t) * 0.2)  
            #print("Drive ID = " + str(t) +"  " + str(candle.md80s[self.index].getId()) + " Position: "  + str(candle.md80s[self.index].getPosition()) + " Velocity: "  + str(candle.md80s[self.index].getVelocity()) )
            time.sleep(0.01)  # Add some delay
    
    def set_pid_mode(self):
        self.candle.controlMd80Mode(self.motor_id, pyCandle.POSITION_PID)     # Set mode to impedance control
        print(self.index)
        self.candle.md80s[self.index].setPositionControllerParams(100.0, 2.2, 0, 30.0)
        self.candle.md80s[self.index].setVelocityControllerParams(100.0, 2.1, 0, 50)
        self.candle.md80s[self.index].setMaxVelocity(50.0)
        self.candle.md80s[self.index].setMaxTorque(50.5)
        print(f"motor {self.motor_id} move to PID mode")
        time.sleep(0.1)
    
    def update_motor_actual_metadata(self):
        self.actual_data.actual_position = self.candle.md80s[self.index].getPosition()
        self.actual_data.act_vel = self.candle.md80s[self.index].getVelocity()
    
    def go_to_limit(self):
        """
        Goto to the limit, each motor has its limit on upper/lower side, conf it by rotation_side
        """
        self.update_motor_actual_metadata()
        curr_pos = self.actual_data.actual_position
        time.sleep(0.5)
        while self.in_allowed_range:
            curr_pos -= (self.joints_params["limit_direction"] * self.calibration_delta)
            self.candle.md80s[self.index].setTargetPosition(curr_pos)
            if(self.limits.limits[self.name]== False):
                print(f"Motor: {self.name} just found his limit")
                self.in_allowed_range = False
            time.sleep(0.1)
        print(f"Calibrator - motor {self.name} just found its limit")
        return curr_pos  # return the last known motor position


    def go_to_zero(self, limit_pos):
        """
        Goto offset zero which is half of the range + the limit's hw offset
        """
        offset_and_half_range = (self.joints_params["max_position"] + self.joints_params["limit_offset"])
        ref_zero_pos = limit_pos + self.joints_params["limit_direction"] * offset_and_half_range
        range_to_zero = np.arange(
            limit_pos,
            ref_zero_pos,
            self.joints_params["limit_direction"] * self.calibration_gesture_params["delta_pos"],
        )  # TODO change to generator list object (Lazy list)
        for i in range(len(range_to_zero)):
            self.candle.md80s[self.index].setTargetPosition(range_to_zero[i])
            time.sleep(0.1)

        time.sleep(0.5)
        print(f"Calibrator - motor {self.name} is now in its Zero pos")
    
          
