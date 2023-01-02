import pyCandle
import time
import calibrator
from limitsI2c import limitsI2c
import utils


if __name__ == "__main__":

    utils.config_yaml()
    cfg = utils.yaml_conf.hardware
    candle = pyCandle.Candle(pyCandle.CAN_BAUD_8M, True)
    limits = limitsI2c()
    
    calibrator.Calibrator(cfg, limits, candle)
    time.sleep(0.1)

    candle.end()
