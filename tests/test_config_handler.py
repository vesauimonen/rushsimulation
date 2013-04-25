import os
import unittest
import json

from rushsimulation.config_handler import ConfigHandler


class TestConfigHandler(unittest.TestCase):

    def test_handle_with_default_configs(self):
        path = os.path.join(os.path.curdir, 'tests/test_config.json')
        config_handler = ConfigHandler(json.load(open(path)))
        user_configs = config_handler.handle()
        self.assertEqual(
            user_configs,
            {
                u'Simulation': {
                    u'debugGraphicAlpha': 0,
                    u'doorSize': 50,
                    u'vehicleAmount': 20
                },
                u'Vehicle': {
                    u'diameter': 15,
                    u'mass': 50,
                    u'maxForce': 14,
                    u'maxSpeed': 8
                }
            }
        )

    def test_string_to_default_int(self):
        config_handler = ConfigHandler(
            {
                u'Simulation': {
                    u'debugGraphicAlpha': 0,
                    u'doorSize': 'String',
                    u'vehicleAmount': 20
                },
                u'Vehicle': {
                    u'diameter': 15,
                    u'mass': 50,
                    u'maxForce': 14,
                    u'maxSpeed': 8
                }
            }
        )
        user_configs = config_handler.handle()
        self.assertEqual(
            user_configs['Simulation']['doorSize'], 50
        )

    def test_clip_to_min(self):
        config_handler = ConfigHandler(
            {
                u'Simulation': {
                    u'debugGraphicAlpha': 0,
                    u'doorSize': -1,
                    u'vehicleAmount': 20
                },
                u'Vehicle': {
                    u'diameter': 15,
                    u'mass': 50,
                    u'maxForce': 14,
                    u'maxSpeed': 8
                }
            }
        )
        user_configs = config_handler.handle()
        self.assertEqual(
            user_configs['Simulation']['doorSize'], 30
        )

    def test_clip_to_max(self):
        config_handler = ConfigHandler(
            {
                u'Simulation': {
                    u'debugGraphicAlpha': 0,
                    u'doorSize': 1000,
                    u'vehicleAmount': 20
                },
                u'Vehicle': {
                    u'diameter': 15,
                    u'mass': 50,
                    u'maxForce': 14,
                    u'maxSpeed': 8
                }
            }
        )
        user_configs = config_handler.handle()
        self.assertEqual(
            user_configs['Simulation']['doorSize'], 80
        )

if __name__ == '__main__':
    unittest.main()
