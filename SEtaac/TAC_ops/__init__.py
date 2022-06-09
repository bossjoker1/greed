
# This is the object exported from Gigahorse
class TAC_Statement:
    def __init__(self, TACblock_ident, ident, opcode, operands=None, defs=None, values=None):
        self.tac_block_id = TACblock_ident
        self.ident = ident
        self.opcode = opcode
        self.operands = operands if operands else list()
        self.defs = defs if defs else list()
        self.values = values if values else dict()
    
    def __str__(self):
        return "TACStatement[blockid:{}|stmtid:{}] | opcode: {} | operands:{} | defs:{} | values:{}".format(self.tac_block_id, 
                                                                                                            self.ident,
                                                                                                            self.opcode, 
                                                                                                            self.operands,
                                                                                                            self.defs,
                                                                                                            self.values)