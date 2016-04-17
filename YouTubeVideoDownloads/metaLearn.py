class meta(type):
    def __new__(cls, class_name, parents, attributes):
        print "class create:",class_name
        return super(meta, cls).__new__(cls, class_name, parents, attributes)
    def __call__(self, *args, **kwargs):
        print "class call"
        return super(meta, self).__call__(*args, **kwargs)

class C(object):
    __metaclass__ = meta

class D(object):
    __metaclass__ = meta
       
if __name__=="__main__":
    pass