#!/bin/bash
python runBackgroundService.py &
python runserver 0.0.0.0:80 &