import time  
from motor import Motor

class Calibrator:
    def __init__(self, cfg, limits, candle):
        self.cfg = cfg
        self.limits = limits
        self.candle = candle
        self.motors = {}
        self.motors_can_ids = []
        self.motor_id2rigid_body = dict((int(k.split()[-1]), v) for k, v in cfg.mapping.items())
        self.rigid_body2motor_id = dict(map(reversed, self.motor_id2rigid_body.items()))
        index = 0
        for motor in self.cfg.robot_params.joints_params:
            name = cfg.robot_params.joints_params[motor]["name"]
            can_id = self.rigid_body2motor_id[name]
            self.motors[can_id] = Motor(cfg, name=name, motor_id=can_id, mot_index = index, limits = limits, candle = candle)
            index +=1
            self.motors_can_ids.append(can_id)
            
            
        # self.motor_controller = motor_controller
        #candle.begin()
        #self.motor_controller.motors[104].move_motor()
        # print("hello")
        
        self.motors_by_name = {}
        # for motor in self.motor_controller.motors:
        #     self.motors_by_name[self.motor_controller.motors[motor].name] = self.motor_controller.motors[motor]
        for motor in self.motors:
            self.motors_by_name[self.motors[motor].name] = self.motors[motor]

        for motor in self.motors_by_name:
            motors_to_calibrate = [motor]#[motors_list[i], motors_list[i+1]]
            user_input = input(f"Do you want to calibrate: {motors_to_calibrate} ?" )
            if user_input == "y" or user_input == "yes":
                print(f"calibrating {motors_to_calibrate}")
                self.calibrate(self.motors_by_name[motor])
                print(f"result of calibyration ")
            else:
                print(f"Not calibrating {motors_to_calibrate}. Moving on")
            
            
    def calibrate(self, motor):
        # err_msg = f"[Motor: {self.name}] Starting calibration is only allowed when motor status is {MotorStatus.IDLE}/{MotorStatus.ERROR}, but motor status is {self.status}."
        # assert self.status in [MotorStatus.IDLE, MotorStatus.ERROR], err_msg
        print(f"Calibrator - {motor.name}")
        # Need to disable motor OR put in idle/safe state
        # time.sleep(0.1)
        motor.set_pid_mode()
        motor.publish_enable_cmd()
        time.sleep(0.1)
        self.candle.begin()
        for motor in self.motors_by_name:
            motor.stay_in
        lowest_pos = motor.go_to_limit()
        time.sleep(0.1)
        motor.go_to_zero(lowest_pos)
        time.sleep(5)
        # motor.update_mode(ControlMode.IMPEDANCE.name)
        self.candle.end()
        motor.publish_zero_cmd()
        print(f"Calibrator - Done with Calibrating {motor.name}")