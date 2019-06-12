'''
Configuration manager.
'''
import yaml
import os
from utils import create_dir

def init(env):
    if env == 'dev':
        cfg = TestConfig()
        return cfg
    else:
        raise ValueError("Unsupported Config.")

class Config:

    @classmethod
    def read_cfg(self, fname):
        with open(fname, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

        self.path     = os.path.join(cfg['paths']['datadir'], 
                                     cfg['paths']['name'], 
                                     cfg['paths']['folder'])

        self.dumpdir  = os.path.join(cfg['paths']['datadir'],
                                     cfg['paths']['name'], 'graph');
        create_dir(self.dumpdir)
        self.astdir   = os.path.join(cfg['paths']['datadir'],
                                     cfg['paths']['name'], 'AST');
        create_dir(self.astdir)
        self.traindir = os.path.join(self.dumpdir, 'train')              
        create_dir(self.traindir)
        self.testdir  = os.path.join(self.dumpdir, 'test')               
        create_dir(self.testdir)
        self.valdir   = os.path.join(self.dumpdir, 'val')               
        create_dir(self.valdir)

class TestConfig(Config):
      def __init__(self):
          self.read_cfg("cfg/config-bert.yml")
          self.verbose = False 
