class FooMeta(type):
    def __new__(cls, name, bases, attrs):
        #attrs['__init__'] = substitute_init
        print 'new obj'
        return super(FooMeta, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        print 'init obj'
        return super(FooMeta, cls).__init__( name, bases, attrs)
    
global_reference={}
class OneThing(object):
    def __new__(cls, *args,**kwargs):   
        for key,value in global_reference.items():
            print key,
            if key==args[0]:
                print 'find old object !'
                return value
        print 'create new object:',args[0]
        newObj=super(OneThing,cls).__new__(cls)
        global_reference[args[0]]=newObj
        return newObj
    def __init__(self,description):
        self.description=description
        
    def display(self):
        print "this is:",self.description
        print "self is:",self
        
        
if __name__=='__main__':
    one=OneThing('123')
    one.display()
    one.abc='efg'
    two=OneThing('123')
    two.display()
    print 'other obj:',two.abc
    print one==two