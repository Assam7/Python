# Submitter anismail(Ismail, Assam)
from goody import type_as_str  # Useful for some exceptions

class DictList:
    def __init__(self,*args):
        temp = []
        count = 0
        for x in args:
            if type(x) is list:
                for y in x:
                    temp.append(y)
                    count = 1
            dictionary = temp
        if count != 1:
            dictionary = list(args)
        self.dl = dictionary
        if len(dictionary) == 0:
            raise AssertionError(f"{dictionary} Cannot be empty")
        for x in dictionary:
            assert type(x) is dict or type(x) is DictList,"Must be a dictionary"
            assert len(x) > 0,"Not a valid dictionary"
    def __len__(self):
        keys = set()
        for x in self.dl:
            for y in x.keys():
                keys.add(y)
        return len(keys)
    def __bool__(self):
        if len(self.dl) ==1:
            return False
        else:
            return True
    def __repr__(self):
        string = ''
        for x in self.dl:
            string+= f'{str(x)},'
        total = string[0:-1]
        return f'DictList({total})'
    def __contains__(self,item):
        count = 0
        for dictionary in self.dl:
            for key in dictionary.keys():
                if item == key:
                    count+=1
                    return True
        if count == 0:
            return False
    def __getitem__(self,item):
        count = 0
        value = 0
        for dictionary in self.dl:
            for key in dictionary.keys():
                if item == key:
                    count+=1
                    value = dictionary[item]
        if count == 0:
            raise KeyError(f"{item} not found in dictionary") 
        return value
    def __setitem__(self,item,value):  
        count = 0
        count1 = 0
        for dictionary in self.dl:
            for key in dictionary.keys():
                if item == key:
                    index = count
                    count1+=1
            count += 1
        if count1 == 0:
            self.dl.append({item:value})
        else:
            examine = self.dl[index]
            examine[item] = value
    def __delitem__(self,item):
        count = 0
        count1 = 0
        for dictionary in self.dl:
            for key in dictionary.keys():
                if item == key:
                    index = count
                    count1+=1
            count+=1
        if count1 == 0:
            raise KeyError(f"{item} not found in dictionary")
        else:
            del self.dl[index][item]
            for x in self.dl:
                if len(x) == 0:
                    self.dl.remove(x)
    def __call__(self,item):
        count = 0
        count1 = 0
        value = []
        for dictionary in self.dl:
            for key in dictionary.keys():
                if item == key:
                    val = (count,dictionary[item])
                    value.append(tuple(val))
                    count1+=1
            count +=1
        if count1 == 0:
            return []
        else:
            return value
    def __iter__(self):
        integrated = set()
        for i in reversed(range(len(self.dl))):
            for y in self.dl[i]:
                if y not in integrated:
                    integrated.add(y)
                    yield y
    def items(self):
        integrated = set()
        for i in reversed(range(len(self.dl))):
            for y in self.dl[i]:
                value = (y,self.__getitem__(y))
                if value not in integrated:
                    integrated.add(tuple(value))
                    yield value
    def collapse(self):
        newDiction = {}
        for diction in self.dl:
            for k in diction:
                newDiction.update({k:diction[k]})
        return newDiction
    def __eq__(self,d1):
        if type(d1) is not DictList and type(d1) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        confirm = True
        if type(d1) is DictList:
            for diction in self.dl:
                for val in sorted(diction.keys(), key=None, reverse=False):
                    for diction1 in d1.dl:
                        for val1 in sorted(diction1.keys(), key=None, reverse=False):
                            if val == val1:
                                if self.__getitem__(val) != d1.__getitem__(val1):
                                    confirm = False
        else:
            for diction in self.dl:
                for val in sorted(diction.keys(), key=None, reverse=False):
                    for val1 in sorted(d1.keys(), key=None, reverse=False):
                        if val == val1:
                            if self.__getitem__(val) != d1.__getitem__(val1):
                                confirm = False
                        else:
                            if val not in d1.keys():
                                confirm = False
        return confirm
    def __lt__(self,d1):
        Sset = set()
        Dset = set()
        if type(d1) is not DictList and type(d1) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        confirm = True
        if type(d1) is DictList:
            for diction in self.dl:
                for val in sorted(diction.keys(), key=None, reverse=False):
                    Sset.add(val)
                    for diction1 in d1.dl:
                        for val1 in sorted(diction1.keys(), key=None, reverse=False):
                            Dset.add(val1)
                            if val == val1:
                                if self.__getitem__(val)!= d1.__getitem__(val1):
                                    confirm = False
                                    return confirm
            errors = 0
            if len(Dset)<len(Sset):
                for x in Dset:
                    if x not in Sset:
                        confirm = False
                        errors+=1
                if errors == 0 and (len(Dset) == len(Sset)):
                    confirm = False
            else:
                for x in Sset:
                    if x not in Dset:
                        confirm = False
                        errors+=1
                if errors == 0 and (len(Dset) == len(Sset)):
                    confirm = False
        elif type(d1) is dict:
            for diction in self.dl:
                for val in sorted(diction.keys(), key=None, reverse=False):
                    Sset.add(val)
                    for val1 in sorted(d1.keys(), key=None, reverse=False):
                        Dset.add(val1)
                        if val == val1:
                            if self.__getitem__(val) != d1.__getitem__(val1):
                                confirm = False
                                return confirm
            errors = 0
            if len(Dset)<len(Sset):
                for x in Dset:
                    if x not in Sset:
                        confirm = False
                        errors+=1
                if errors == 0 and (len(Dset) == len(Sset)):
                    confirm = False
            else:
                for x in Sset:
                    if x not in Dset:
                        confirm = False
                        errors+=1
                if errors == 0 and (len(Dset) == len(Sset)):
                    confirm = False
        return confirm
    def __gt__(self,d1):
        if type(d1) is not DictList and type(d1) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        if type(self) is not DictList and type(self) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        if type(self) is DictList and type(d1) is DictList:
            return d1 < self
        elif type(self) is DictList and type(d1) is dict:
            return self < d1
        elif type(self) is dict and type(d1) is DictList:
            return d1.__lt__(self)
    def __add__(self,d1):
        if type(d1) is not DictList and type(d1) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        values = []
        if type(self) is DictList and type(d1) is DictList:
            for x in list(self.dl):
                total = {k:v for k,v in x.items()}
            values.append(total)
            for y in list(d1.dl):
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
        elif type(self) is dict and type(d1) is DictList:
            for x in list(self):
                total = {k:v for k,v in x.items()}
            values.append(total)
            for y in list(d1.dl):
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
        elif type(self) is DictList and type(d1) is dict:
            for x in list(self.dl):
                total = {k:v for k,v in x.items()}
            values.append(total)
            for y in [d1]:
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
        obj = DictList(values)
        return obj
    def __radd__(self,d1):
        if type(d1) is not DictList and type(d1) is not dict:
            raise TypeError("Must be of type Dictlist or of type dict")
        values = []
        if type(self) is DictList and type(d1) is DictList:
            for y in list(d1.dl):
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
            for x in list(self.dl):
                total = {k:v for k,v in x.items()}
            values.append(total)
        elif type(self) is dict and type(d1) is DictList:
            for y in list(d1.dl):
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
            for x in list(self):
                total = {k:v for k,v in x.items()}
            values.append(total)
        elif type(self) is DictList and type(d1) is dict:
            for y in [d1]:
                total1 = {k:v for k,v in y.items()}
            values.append(total1)
            for x in list(self.dl):
                total = {k:v for k,v in x.items()}
            values.append(total)
        obj = DictList(values)
        return obj
    def __setattr__(self,name,value):
        if len(self.__dict__) == 0:
            self.__dict__.update({name:value})
        else:
            raise AssertionError("Cannot add any new attributes")
    
if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test DictList before doing bsc tests
    
    d = DictList(dict(a=1,b=2), dict(b=12,c=13))
    print('len(d): ', len(d))
    print('bool(d):', bool(d))
    print('repr(d):', repr(d))
    print(', '.join("'"+x+"'" + ' in d = '+str(x in d) for x in 'abcx'))
    print("d['a']:", d['a'])
    print("d['b']:", d['b'])
    print("d('b'):", d('b'))
    print('iter results:', ', '.join(i for i in d))
    print('item iter results:', ', '.join(str(i) for i in d.items()))
    print('d.collapse():', d.collapse())
    print('d==d:', d==d)
    print('d+d:', d+d)
    print('(d+d).collapse():', (d+d).collapse())
    
    print()
    import driver
    driver.default_file_name = 'bsc22S20.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
