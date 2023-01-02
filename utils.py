import logging
import argparse
from hydra import compose, initialize
from omegaconf import OmegaConf
import argparse


def config_yaml(self):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--yaml", default="configs/default.yaml", help="Configuration file")
    args, unknown = parser.parse_known_args()
    yaml_path_split = args.yaml.split("/")
    config_path = "/".join(yaml_path_split[:-1])
    config_name = yaml_path_split[-1][:-5]
    with initialize(config_path=config_path, job_name="mentor_app"):
        yaml_conf = compose(config_name=config_name,
                            overrides=["hydra.run.dir=/tmp"])
        # Struct to normal :)
        yaml_conf = OmegaConf.to_container(yaml_conf)
        yaml_conf = OmegaConf.create(yaml_conf)


# def config_logger(self):
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)
#     logger.addHandler(logging.StreamHandler())
#     logger.info("starting motor controller node")
