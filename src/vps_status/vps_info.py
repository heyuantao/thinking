import requests
from BandwagonHost import BandwagonHost
import json

if __name__=="__main__":
   id="197997"
   key="private_iXuEESKJiosuVuKzeru3ACAr"
   
   bandwagonHost=BandwagonHost(id,key)
   print bandwagonHost.getBasicInformation()
   print bandwagonHost.getServiceInformation()
   #print bandwagonHost.getAvailableOS()
   print bandwagonHost.startOS()