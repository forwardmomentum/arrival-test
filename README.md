### Transport Agency application

#### Architecture

1. Agency Server

2. Drivers Emulator

#### Run

1. Run Rabbitmq and Postgres with ```docker-compose up ```
2. Run ```python drivers_data_generator.py <drivers_num>``` to generate data for <drivers_num> drivers (e. g. 20)
3. Run ```python agency_server/agency_server.py``` to start agency server on 9001
4. In another terminal window run ```python drivers-emulator/drivers-emulator.py``` to run drivers emulator service


