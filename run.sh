python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip

pip3 install pytest
pip3 install coverage

#export PYTHONPATH="${PYTHONPATH}:Users/igor/Documents/Research/TestAmplification/library/flair"
pip3 install -r requirements.txt
# PYTHONPATH="/Users/igor/Documents/Research/TestAmplification/library" coverage run -m pytest library
# coverage run -m pytest .

#pip3 install -r dependencies/jina/requirements.txt

#export PYTHONPATH="${PYTHONPATH}:Users/igor/Documents/Research/TestAmplification/dependencies/BERTopic/bertopic"
# PYTHONPATH="/Users/igor/Documents/Research/TestAmplification/dependencies/TextAttack" coverage run --source=flair -m pytest dependencies/TextAttack

# coverage html
# mv ./cov_html ./cov_html_flair

echo "Hallo"
INPUT=users.txt
OLDIFS=$IFS

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while IFS=, read -r project src tests github;
do
	echo "Name : $project"
	echo "src : $src"
	echo "tests : $tests"
	echo "github : $github"

  git clone "$github"
  mv $project/$src tmp
  mv $project/$tests/* tests
  pip3 install -r ./$project/requirements.txt
  pip3 install tensorflow_text
  rm -rf $project
  mv tmp $src

  SCRIPTPATH="$( cd -- "$(dirname "$src")/$src" >/dev/null 2>&1 ; pwd -P )"
  echo "Scriot"
  echo $SCRIPTPATH
  PYTHONPATH=$SCRIPTPATH coverage run --source=flair -m pytest .
  coverage html
#   mv ./htmlcov ./htmlcov_$project

done < $INPUT
IFS=$OLDIFS

echo "Done"
