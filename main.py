if __name__ == '__main__':
    import json
    from rushsimulation.simulation import RushApp
    from rushsimulation.config_handler import ConfigHandler
    config_handler = ConfigHandler(json.load(open('config.json')))
    user_configs = config_handler.handle()
    RushApp(user_configs=user_configs).run()
