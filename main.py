if __name__ == '__main__':
    import os
    import json
    from rushsimulation.simulation import RushApp
    from rushsimulation.config_handler import ConfigHandler
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    config_handler = ConfigHandler(json.load(open(path)))
    user_configs = config_handler.handle()
    RushApp(user_configs=user_configs).run()
