# Install
sudo python setup.py install
sudo rm -rf namekox_amqp.egg-info build dist

# Upload
sudo pip install -U setuptools wheel twine
sudo python setup.py sdist bdist_wheel
sudo twine upload dist/*
sudo rm -rf namekox_amqp.egg-info build dist
