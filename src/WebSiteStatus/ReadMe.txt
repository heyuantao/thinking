Files Description

1:SiteStatusService
   This is not python app,just normal python package
   this package is used by runBackgroundService.py file to start the check service.The service will check the web url every 
one minute.

2:WebSiteStatus
   This is Django created default package for setting and other things
   
3:MainApplication
   Most of view were implement in this package
   
How to use 
1.run the command,python 2.7 was tested 
  python runBackgroundService.py 
2.run the command
  python runserver 0.0.0.0:80
  the django program will be started and communicate with backgroud service with redis
  
