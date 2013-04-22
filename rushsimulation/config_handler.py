class ConfigHandler(object):
    """
    A simple JSON config validator.
    """
    def __init__(self, config):
        self.config = config

    def handle(self):
        self.handle_simulation_configs()
        self.handle_vehicle_configs()
        return self.config

    def handle_simulation_configs(self):
        DOOR_SIZE = [30, 80, 50]
        VEHICLE_AMOUNT = [1, 20, 15]
        DEBUG_GRAPHIC_ALPHA = [0, 1, 0]
        self.config['Simulation']['doorSize'] = self.validate(
            self.config['Simulation']['doorSize'],
            DOOR_SIZE[0],
            DOOR_SIZE[1],
            DOOR_SIZE[2]
        )
        self.config['Simulation']['vehicleAmount'] = self.validate(
            self.config['Simulation']['vehicleAmount'],
            VEHICLE_AMOUNT[0],
            VEHICLE_AMOUNT[1],
            VEHICLE_AMOUNT[2]
        )
        self.config['Simulation']['debugGraphicAlpha'] = self.validate(
            self.config['Simulation']['debugGraphicAlpha'],
            DEBUG_GRAPHIC_ALPHA[0],
            DEBUG_GRAPHIC_ALPHA[1],
            DEBUG_GRAPHIC_ALPHA[2]
        )

    def handle_vehicle_configs(self):
        MAX_SPEED = [3, 12, 8]
        MAX_FORCE = [10, 20, 14]
        DIAMETER = [5, 20, 15]
        self.config['Vehicle']['maxSpeed'] = self.validate(
            self.config['Vehicle']['maxSpeed'],
            MAX_SPEED[0],
            MAX_SPEED[1],
            MAX_SPEED[2]
        )
        self.config['Vehicle']['maxForce'] = self.validate(
            self.config['Vehicle']['maxForce'],
            MAX_FORCE[0],
            MAX_FORCE[1],
            MAX_FORCE[2]
        )
        self.config['Vehicle']['diameter'] = self.validate(
            self.config['Vehicle']['diameter'],
            DIAMETER[0],
            DIAMETER[1],
            DIAMETER[2]
        )

    def validate(self, value, min, max, default):
        if value and not isinstance(value, basestring):
            if value > max:
                return max
            if value < min:
                return min
            return value
        return default
