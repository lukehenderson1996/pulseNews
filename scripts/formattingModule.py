'''Short description'''

# Author: xxxxx
__version__ = '0.0'

'external imports here'

'internal imports here'

class NAME: #or, ClassName
    '''NAME class'''
    internalConstant = 2e-6

    def __init__(self, arg1, arg2, optionalArg3='normal'):
        '''Short description\n
        Args:
            arg1 [str]: description\n
            arg2 [float]: description\n
            optionalArg3 [str, optional]: 
                long description------------------------
        Return:
            [int] 0 for pass
        Notes:
            notes here'''
        #internal automatically called init code here
        self.internalVariable = 'variable content'
        pass

    def init(self):
        '''non-automatic init'''
        pass

    def _internalFunction(self, arg1):
        pass

    def publicFunction(self, arg1, arg2) -> float:
        return 2.3