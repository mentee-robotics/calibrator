import pyCandle
import time, logging, argparse  
from hydra import compose, initialize
from omegaconf import OmegaConf
import calibrator 
from limitsI2c import limitsI2c


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logger.addHandler(logging.StreamHandler())
    logger.info("starting motor controller node")

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", default="configs/default.yaml", help="Configuration file")

    args, unknown = parser.parse_known_args()

    # Configuring hydra
    yaml_path_split = args.yaml.split("/")
    config_path = "/".join(yaml_path_split[:-1])
    config_name = yaml_path_split[-1][:-5]
    with initialize(config_path=config_path, job_name="mentor_app"):
        yaml_conf = compose(config_name=config_name, overrides=["hydra.run.dir=/tmp"])
        # Struct to normal :)
        yaml_conf = OmegaConf.to_container(yaml_conf)
        yaml_conf = OmegaConf.create(yaml_conf)

    cfg = yaml_conf.hardware
    candle = pyCandle.Candle(pyCandle.CAN_BAUD_8M, True)
    limits = limitsI2c()
    calibrator = calibrator.Calibrator(cfg, limits, candle)
    time.sleep(0.1)
    # motors_controller.init_motors_publisher_loop()
    # rate = rospy.Rate(COMM_FREQ)
    candle.end()
   # try:
    #    motors_controller.run()
    #except rospy.ROSInterruptException:
    #    logger.error("EXCEPTION EXCEPTION")
    #    pass