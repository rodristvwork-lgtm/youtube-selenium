# youtube-selenium Firefox
Steps to install youtube buffer catcher using selenium with Firefox

# Create Environment
python3 -m venv .venv

# Activate Environment Python
source .venv/bin/activate

# To install requirements
pip install -r requirements.txt

# Download driver
python get_mozilla_selenium_driver.py

# Run Youtube buffer catcher
python youtube.py

# Deactivate Environment
deactivate
