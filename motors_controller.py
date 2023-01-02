from motor import Motor


class MotorsController:
    def __init__(self, cfg, limits) -> None:
        self.cfg = cfg
        self.motors = {}
        self.motors_can_ids = []
        self.motor_id2rigid_body = dict((int(k.split()[-1]), v) for k, v in cfg.mapping.items())
        self.rigid_body2motor_id = dict(map(reversed, self.motor_id2rigid_body.items()))
        index = 0
        for motor in self.cfg.robot_params.joints_params:
            name = cfg.robot_params.joints_params[motor]["name"]
            can_id = self.rigid_body2motor_id[name]
            self.motors[can_id] = Motor(cfg, name=name, motor_id=can_id, mot_index = index, limits = limits)
            index +=1
            self.motors_can_ids.append(can_id)
        
    
        # self.motors[104].set_pid_mode()
    
        # self.motors[104].publish_enable_cmd()
   
    
    def run(self):
        print("running")