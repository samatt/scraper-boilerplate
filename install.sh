sudo apt-get update

sudo apt-get install -y firefox htop git python-dev build-essential xvfb python3-pip
sudo pip3 install -U -r requirements.txt

# Install specific version of Firefox known to work well with the selenium version above
if [ $(uname -m) == 'x86_64' ]; then
  echo Downloading 64-bit Firefox
  wget https://ftp.mozilla.org/pub/firefox/releases/45.9.0esr/linux-x86_64/en-US/firefox-45.9.0esr.tar.bz2
else
  echo Downloading 32-bit Firefox
  wget https://ftp.mozilla.org/pub/firefox/releases/45.9.0esr/linux-i686/en-US/firefox-45.9.0esr.tar.bz2
fi
tar jxf firefox*.tar.bz2
rm -rf firefox-bin
mv firefox firefox-bin
rm firefox*.tar.bz2

# Need geckodrivers https://github.com/SeleniumHQ/selenium/blob/master/py/docs/source/index.rst#drivers
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar xzf geckodriver-*.tar.gz
mv geckodriver /usr/bin/geckodriver