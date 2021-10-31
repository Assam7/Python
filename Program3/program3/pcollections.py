# Submitter anismail(Ismail, Assam)
import re, traceback, keyword    
def pnamedtuple(type_name, field_names, mutable= False, defaults= {}):
    def show_listing(s):
        for line_number, line_text in enumerate(s.split('\n'),1):  
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    def unique(field_names):
        iterated = list()
        for i in field_names:
            if i not in iterated:
                iterated.append(i)
        return iterated
    compare = bool(re.match('[a-zA-Z]([a-zA-Z\d_])*', str(type_name)))
    if compare == False:
        raise SyntaxError("Must be a legal name!")
    if type(field_names) not in (list,str):
        raise SyntaxError("Not a legal type!")
    if type(field_names) in (list,str):
        if type(field_names) is str:
            field = [x for x in field_names.split(' ') if x!='']
            value = []
            for x in field:
                value.append(x.replace(',',''))
            field = value
        else:
            field = [x for x in field_names if x.isalpha() == True or x.isdigit()==True]
        for x in field:
            if x in keyword.kwlist:
                raise SyntaxError("Cannot be a key word")
            compare = bool(re.match('[a-zA-Z]([a-zA-Z\d_])*', x))
            if compare == False:
                print("Error")
                raise SyntaxError("Must be a legal name!")
    field_names1 = unique(field)
    for k,v in defaults.items():
        if k not in field_names1:
            raise SyntaxError("Key not in field names")
    def gen_init(field_names1):
        string = "    def __init__(self,{field}):\n        self._fields = {field_names}\n        self._mutable = {mutable}\n        "
        for x in field_names1:
            string+=f"self.{str(x)} = {str(x)}\n        "
        return string.format(field = ','.join([item for item in field_names1]),type_name=type_name,mutable = mutable,field_names = field_names1)
    def reprString(field_names1):
        string = "    def __repr__(self):\n         return f'{type_name}(".format(type_name=type_name)
        for x in field_names1:
            string += x+"={self."+x+'},'
        return (string[:-1] + ")'")
    def get_(field_names1):
        string = ''
        for variable in field_names1:
            string += "    def get_"+variable+"(self):\n        return self."+variable+"\n"
        return string
    def get_item():
        string = \
        '''
    def __getitem__(self,index):
        if type(index) not in (int,str):
            raise IndexError("Must be of type string or of type int!")
        elif type(index) is str:
            if index not in self._fields:
                raise IndexError(f"{index} not a valid index in field names")
            else:
                return self.__dict__[index]
        elif type(index) is int:
            if index < len(self._fields):
                return self.__dict__[self._fields[index]]
            else:
                raise IndexError("Out of bounds error!")
        '''
        return string
    def isEqual():
        string= \
    '''
    def __eq__(self,other):
        return repr(self) == repr(other)
    '''
        return string
    def _asdict(type_name,field_names1):
        string1 =''
        for x in field_names1:
            string1 +="diction.update({'"+x+"': self.get_"+x+"()})\n        "
        string = \
        '''
    def _asdict(self):
        diction = dict()
        {string1}
        return diction
    '''
        return string.format(string1=string1)
    def make(type_name):
        string = \
        '''
    def _make(iterable):
        string1 = "{type_name}("
        for item in iterable:
            string1+=str(item)+","
        string2 = string1[:-1]+')'
        return eval(string2)
        '''
        return string.format(type_name=type_name)
    def replace():
        string = \
        '''
    def _replace(self,**kargs):
        if self._mutable:
            for k,v in kargs.items():
                if k in self._fields:
                    self.__dict__[k] = v
                else:
                    raise TypeError("Must be a legal type and exist in the field")
            otherObject = None
        else:
            otherObject = eval(repr(self))
            for k,v in kargs.items():
                if k in otherObject._fields:
                    otherObject.__dict__[k] = v
                else:
                    raise TypeError("Must be a legal key in the field")
        return otherObject
        '''
        return string
    def setAttr():
        string = \
        '''
    def __setattr__(self,name,value):
        if name in self.__dict__:
            if self._mutable:
                self.__dict__[name] = value
            else:
                raise AttributeError("cannot add any new attributes because mutability is False")
        else:
            self.__dict__[name] = value
        '''
        return string
    initstring = gen_init(field_names1)
    reprString1 = reprString(field_names1)
    getString = get_(field_names1)
    getitemString = get_item()
    equalBool = isEqual()
    dictString = _asdict(type_name,field_names1)
    makeString = make(type_name)
    replaceS = replace()
    setString = setAttr()
    class_definition1 = \
    '''
class {type_name}:
{initstring}
{reprString1}
{getString}
{getitemString}
{equalBool}
{dictString}
{makeString}
{replaceS}
{setString}

    '''
    class_definition = class_definition1.format(type_name=type_name,initstring=initstring,reprString1 = reprString1,getString = getString,getitemString=getitemString,equalBool=equalBool,dictString=dictString,makeString=makeString,replaceS=replaceS,setString=setString)

    # To help debug, uncomment next line, which shows source code for the class
    show_listing(class_definition)
    
    # Execute the class_definition (str), in a special name space; then bind its
    #   source_code attribute to class_definition; following try/except return
    #   the class object created; if there is a syntax error, show the class
    #   and also show the error
    name_space = dict( __name__ = 'pnamedtuple_{type_name}'.format(type_name=type_name) )        
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):            
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]
    

    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S20.txt'
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
