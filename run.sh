

python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip

pip3 install pytest
pip3 install coverage

#export PYTHONPATH="${PYTHONPATH}:Users/igor/Documents/Research/TestAmplification/library/flair"
pip3 install -r requirements.txt
# PYTHONPATH="/Users/igor/Documents/Research/TestAmplification/library" coverage run -m pytest library
coverage run -m pytest .

#pip3 install -r dependencies/jina/requirements.txt

#export PYTHONPATH="${PYTHONPATH}:Users/igor/Documents/Research/TestAmplification/dependencies/BERTopic/bertopic"
# PYTHONPATH="/Users/igor/Documents/Research/TestAmplification/dependencies/TextAttack" coverage run --source=flair -m pytest dependencies/TextAttack

coverage html
