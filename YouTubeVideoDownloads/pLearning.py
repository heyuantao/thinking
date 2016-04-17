
class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._instance

class A(Singleton):
    pass

if __name__=="__main__":
    a1=A();
    a2=A();
    print a1
    print a2
