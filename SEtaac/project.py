import logging
import os 
import dill
import sys 

from datetime import datetime
from SEtaac.cfg import CFG, _import_cfgs_gigahorse
from SEtaac.simulation_manager import SimulationManager
from SEtaac.TAC_parser import TACparser
from SEtaac.state import SymbolicEVMState
from SEtaac.function import TAC_Function
from SEtaac.TAC_parser import TACparser

from .config import *

l = logging.getLogger("project")
l.setLevel(logging.INFO)

class Project(object):
    def __init__(self, binary:str="", cfg_data:str="", onchain_address:str=""):
        
        if binary == "" or cfg_data == "":
            l.fatal("Need gigahorse artifacts to create a project (IR_DICT and TAC_CFG)")
            sys.exit(0)

        # Load the TAC IR from the file dumped with gigahorse
        with open(binary, "rb") as bin_file:
            self.TAC_code_raw = dill.load(bin_file)

        # Load the TAC CFG exported by Gigahorse client
        with open(cfg_data, "rb") as cfgdata_file:
            self.TAC_cfg_raw = dill.load(cfgdata_file)

        # Object that creates other objects
        self.factory = FactoryObjects(TACparser(self.TAC_code_raw))
        self.functions = self._import_functions_gigahorse(self.TAC_cfg_raw)

        # import the web3 provider just in case (from config)
        self.web3 = w3 
        self.onchain_address = onchain_address

        if self.onchain_address != '':
            # if we have an address let's use it as the name of the folder
            self._workspace_folder = os.path.join(WORKSPACE, self.onchain_address)
        else:
            # otherwise, let's use a random 12 chars strings
            self._workspace_folder = os.path.join(WORKSPACE, "project_" + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        # Check whether the specified path exists or not and create the workspace for this project
        isExist = os.path.exists(self._workspace_folder)
        if not isExist:
            os.makedirs(self._workspace_folder)
    
    def _import_functions_gigahorse(self, TAC_cfg_raw:dict):
        funcs = {}
        for _, func_data in TAC_cfg_raw['functions'].items():
            # Just to make sure there are no collision on function addresses
            assert(not funcs.get(func_data["addr"], None))
            funcs[func_data["addr"]] = TAC_Function(func_data["addr"]  , func_data["name"], func_data["is_public"], 
                                                    func_data['blocks'], func_data['arguments'])
        
        return funcs

    #@property
    #def cfg(self):
    #    if not self._cfg:
    #        self._cfg = CFG()
    #    return self._cfg

# This class create object like the simgr, entry_state, etc...
class FactoryObjects:
    def __init__(self, TAC_parser:TACparser):
        self.TAC_parser = TAC_parser
        
    def simgr(self, entry_state:SymbolicEVMState):
        return SimulationManager(entry_state=entry_state)
    
    def entry_state(self, xid:str):
        return SymbolicEVMState(xid=xid)
    
    def block(self, block_id:str):
        return self.TAC_parser.parse(block_id)