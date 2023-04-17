# install the requirements
pip3 install -r requirements.txt

cd /app

export FLASK_APP=flaskr
echo "Existing directory at " $(pwd)

# start the app
python server.py