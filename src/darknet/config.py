import toml
from os.path import abspath, join, dirname

# holds model configuration information
class Config:
    def __init__(self, configPath):
        # load toml config file
        config = toml.load(configPath)
        
        # get the base path to the model folder
        base = dirname(configPath)

        # pull out the obvious things, make the paths absolute
        self.cfgPath = join(base, config["cfg"])
        self.weightsPath = join(base, config["weights"])
        
        # load the names - we'll just go ahead and parse them
        namePath = join(base, config["names"])
        with open(namePath, "r") as f:
            self.names = f.read().strip().split('\n')

# instead of pointing to the config file, just point to the dict containing everything
def loadConfigDir(dictPath):
    base = abspath(dictPath)
    configPath = join(base, "config.toml")
    return Config(configPath)