# Submitter anismail(Ismail, Assam)
from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self,bIter = []):
        self.diction = defaultdict(list)
        for x in bIter:
            if x in self.diction.keys():
                self.diction[x] += 1
            else:
                self.diction[x] = 1
    def __repr__(self):
        temp = []
        for v,c in self.diction.items():
            for i in range(c):
                temp.append(v)
        return f'Bag({temp})'
    def __str__(self):
        string = ''
        for x,y in sorted(self.diction.items()):
            string += f'{x}[{y}],'
        total = string[0:-1]
        return f'Bag({total})'
    def __len__(self):
        count = 0
        for x,y in self.diction.items():
            count+=y
        return count
    def unique(self):
        count = 0
        for k in self.diction.keys():
            count +=1
        return count
    def add(self,value):
        if value in self.diction.keys():
            self.diction[value] += 1
        else:
            self.diction[value] = 1
    def __contains__(self,item):
        if item in self.diction.keys():
            return True
        else:
            return False
    def count(self,item):
        count = 0
        for x in self.diction.keys():
            if x == item:
                count = self.diction[item]
        return count
    def __add__(self,bag1):
        newDiction = {}
        if type(bag1) is not Bag:
            raise TypeError(f"Must be of type Bag")
        for k,v in self.diction.items():
            for y,z in bag1.diction.items():
                if k == y:
                    newDiction[k] = v+z
                else:
                    if k not in newDiction.keys():
                        newDiction[k] = v
                    elif y not in newDiction.keys():
                        newDiction[y] = z
        temp = []
        for k,v in sorted(newDiction.items()):
            for y in range(v):
                temp.append(k)
        obj = Bag(temp)
        return obj            
    def remove(self,item):
        if item in self.diction.keys():
            if self.diction[item] >= 1:
                self.diction[item]-= 1
            else:
                if self.diction[item] == 0:
                    self.diction.pop(item)
                    raise ValueError(f"Cannot remove {item} from dictionary")
    def __eq__(self,b):
        if type(b) is not Bag:
            return False
        if self.diction == b.diction:
            return True
        else:
            return False
    def __iter__(self):
        def gen(bins):
            for k,v in bins.items():
                for i in range(v):
                    yield k
        return gen(dict(self.diction))
if __name__ == '__main__':
    #driver tests
    import driver
    driver.default_file_name = 'bsc21S20.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
