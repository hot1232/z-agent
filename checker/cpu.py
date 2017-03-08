from . import CheckerBase

class Checker(CheckerBase):    
    def do_check_load(self):
        return 16
    
    def do_check_hard_interupt(self):
        return 0
    
    def do_check_soft_interrupt(self):
        return 0
        
        
        
        
        
        
    