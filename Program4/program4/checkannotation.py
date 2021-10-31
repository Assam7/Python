# Submitter anismail(Ismail, Assam)
from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self,check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Start by binding the class attribute to True allowing checking to occur
    #   (but only if the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # Check the decorated function by binding its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive
        def checkTuple():
            if type(value) is not tuple:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be tuple")
            if len(annot) == 1:
                for x in value:
                    check_history = f'tuple[{value.index(x)}] check: {annot[0]}'
                    self.check(param,annot[0], x, check_history)
            else:
                if len(annot) != len(value):
                    raise AssertionError(f"'{param}' failed annotation check(wrong number of elements): value = {value}... annotation had {len(annot)} elements{annot}\n{check_history}")
                else:
                    for x in range(len(value)):
                        check_history = f'tuple[{value[x]}] check: {annot[x]}'
                        self.check(param,annot[x], value[x], check_history)
        def checkStr():
            try:
                val = bool(eval(annot))
                if val == False:
                    raise AssertionError()
            except NameError:
                print()
            except:
                raise AssertionError()
        def checkList():
            if type(value) is not list:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be list")
            if len(annot) == 1:
                for x in value:
                    check_history = f'list[{value.index(x)}] check: {annot[0]}'
                    self.check(param,annot[0], x, check_history)
            else:
                if len(annot) != len(value):
                    raise AssertionError(f"'{param}' failed annotation check(wrong number of elements): value = {value}... annotation had {len(annot)} elements{annot}")
                else:
                    for x in range(len(value)):
                        check_history = f"list[{value[x]} check: {annot[x]}"
                        self.check(param,annot[x], value[x], check_history)
        def checkLambda():
            try:
                l = []
                l.append(value)
                print(value)
                if len(l) != 1:
                    raise AssertionError(f"'{param}' inconsistency: predicate shoukd have one paramter but had {len(l)} predicate = {annot}")
                elif annot.__call__(value) == False:
                    raise AssertionError(f"'{param}' failed annotation check, value = {value} predicate = {annot}")
            except:
                raise AssertionError(f"'{param}' predicate {annot} raised exception")
            
            
        def checkdict():
            if isinstance(value, dict) == False:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be dict")
            for k1,v1 in value.items():
                l = []
                l.append(v1)
                if len(l) > 1:
                    raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be dict")
                else:
                    for k,v in annot.items():
                        self.check(param, k, k1, check_history)
                        self.check(param, v, v1, check_history)
                    
        def checkSet():
            if isinstance(value, set) == False:
                raise AssertionError(f"'{param}' annotation inconsistency: dict should have 1 item but had {len(annot)} annotations: {annot}")
            if len(annot) > 1:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be set")
            if len(annot) ==1:
                for k in annot:
                    for x in value:
                        check_history = f"set {x} check: {k}"
                        if isinstance(x, k) == False:
                            raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be set\n{check_history}")
        def checkFrozen():
            if isinstance(value, frozenset) == False:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be frozenset")
            if len(annot) > 1:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be frozenset")
            if len(annot) ==1:
                for k in annot:
                    for x in value:
                        check_history = f"set {x} check: {k}"
                        if isinstance(x, k) == False:
                            raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be frozenset\n{check_history}")
        if annot is None:
            pass
        elif isinstance(annot,str):
            checkStr()
        elif isinstance(annot, type):
            if isinstance(value, annot) == False:
                raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value}... was type {type(value)} but it should be {type(annot)}")
        elif isinstance(annot, frozenset) == True:
            checkFrozen()
        elif isinstance(annot, set) == True:
            checkSet()
        elif isinstance(annot,list) == True:
            checkList()
        elif isinstance(annot,tuple) == True:
            checkTuple()
        elif isinstance(annot, dict):
            checkdict()
        elif inspect.isfunction(annot):
            checkLambda()
        else:
            try:
                val = annot.__check_annotation__(self.check,param,value,check_history)
                if val == False:
                    raise AssertionError(f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)}... should be {type(annot)}")
            except AttributeError:
                raise AssertionError(f"'{param}' annotation undecipherable: {annot}")
            except:
                raise AssertionError(f"'{param}' annotation predicate{annot} raised exception")
        
        # Start by matching check's function annotation against its arguments 
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        # Return the parameter/argument bindings in an ordereddict, derived
        #   from a dict: it binds the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        if self._checking_on == False or Check_Annotation.checking_on == False:
            return self._f(*args,**kargs)
    
        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            # For each annotation present, check if the parameter satisfies it
            annotDict = self._f.__annotations__
            pBinds_Dictionary = param_arg_bindings()
            # Compute/remember the value of the decorated function
            # If 'return' is in the annotation, check it
            for parameter in pBinds_Dictionary:
                if parameter in annotDict:
                    self.check(parameter,annotDict[parameter], pBinds_Dictionary[parameter], check_history='')
            answer = self._f(*args,**kargs)
            # Return the decorated answer
            
            print(self._f.__annotations__)
            if 'return' in annotDict:
                pBinds_Dictionary['_return'] = answer
                self.check('_return', annotDict['return'], pBinds_Dictionary['_return'])
            return answer
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            raise
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
                #print(l.rstrip())
            #print(80*'-')
            #raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    '''
    def f(x:int): pass
    f = Check_Annotation(f)
    f(3)
    f('a')
    '''
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S20.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
