### Transport Agency application

http://194.177.22.204:9001/

In GUI you can find info about any driver and send message. Follow  

#### Architecture

1. Agency Server

Tornado app, Provides REST+Websocket API for GUI. [Look at code](agency-server/agency_server.py)
 
2. Drivers Emulator

Handles lifecycle of drivers (activates, deactivates them, sends messages). [Look at code](drivers-emulator/drivers_emulator.py)

#### Run

1. Run Rabbitmq and Postgres with ```docker-compose up ```
2. Run ```python3.5 drivers_data_generator.py 
3. Run ```python3.5 agency_server/agency_server.py <drivers_num>``` to generate data for <drivers_num> drivers (e. g. 20)
4. In another terminal window run ```python3.5 drivers-emulator/drivers-emulator.py``` to run drivers emulator service
