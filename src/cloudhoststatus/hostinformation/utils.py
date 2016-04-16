from hostinformation.models import KeyValueStorage

class SystemSettings(object):
    hostIdKeyName="hostId"
    hostSecretKeyName="hostSecret"
    @classmethod
    def getHostId(cls):
        obj,created=KeyValueStorage.objects.get_or_create(key=cls.hostIdKeyName)
        if created is True:
            return ""
        else:
            return obj.value
    @classmethod
    def setHostId(cls,value):
        obj,created=KeyValueStorage.objects.get_or_create(key=cls.hostIdKeyName)
        obj.value=value
        obj.save()
    @classmethod
    def getHostSecret(cls):
        obj,created=KeyValueStorage.objects.get_or_create(key=cls.hostSecretKeyName)
        if created is True:
            return ""
        else:
            return obj.value    
    @classmethod    
    def setHostSecret(cls,value):
        obj,created=KeyValueStorage.objects.get_or_create(key=cls.hostSecretKeyName)
        obj.value=value
        obj.save()