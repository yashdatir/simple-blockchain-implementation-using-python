** Activate Virtual Environment **
```
source blockchain-env/bin/activate
```

** Install all packages **
```
pip3 install -r requirements.txt
```

** Run the Tests **
Make sure to activate virtual environment
```
python3 -m pytest backend/test
```

** Run the application and API **
Make sure to activate virtual environment
```
python3 -m backend.app
```

** Run a peer instance **
Make sure to activate virtual environment
```
export PEER=True && python3 -m backend.app
```

** Run the Frontend **
In the frontend directory,
```
npm run start
```

** SEED the backend with data **
Make sure to activate virtual environment
```
export SEED_DATA=True && python3 -m backend.app
```