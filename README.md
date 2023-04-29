# Indisim Mutual Backend - Flask

## Setting up backend

1. Go to backend directory
2. Start a Virtual Environnment to install all the packages by following the steps in the (documentation)[https://docs.python.org/3/library/venv.html]
3. Install all the requirements from requirements.txt with following command.
   `pip install -r requirements.txt`

### Installing Indisim_mutual package

1. Clone it from this (link)[https://github.com/ShengpeiWang/indisim_mutual.git]. Make sure it is in the same directory as of the backend project.
   `pip install -e PATH\to\local\package`

### Run the Server

`pip install -e ../indisim_mutual && gunicorn --preload --workers 4 --threads 100 main:app --timeout 600`

1. Navigate to the backend directory and make sure all the required packages are installed.
2. Use the following command to start the server.
   `python3 main.py`

### Congratulations, your server is successfully running on port 8000! You can access the end point from your frontend project.

## Setting up frontend

1. Install all the packages for React
   `npm install`
2. To start the frontend server
   `npm start`

## TODO

Back-end

- interact with the model
- figure output for diff. data requests
- csv output for diff. data requests

Front-end

- implement each page
- make api calls
- get dynamic visualization
- figure output for diff. data requests
- csv output for diff. data requests

Hosting

- docker build
- upload
- scale
