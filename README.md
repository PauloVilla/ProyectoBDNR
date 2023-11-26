# ProyectoBDNR
En este repositorio se encuentra el desarrollo del proyecto de la clase de bases de datos no relacionales

### Setup a python virtual env with python pymongo installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r requirements.txt
```

### To run the API service
```
python -m uvicorn main:app --reload
```

### To load data
Ensure you have a running mongodb instance
i.e.:
```
docker run --name mongodb -d -p 27017:27017 mongo
```
Once your API service is running (see step above), run the populate script
```
python3 populate.py
```
