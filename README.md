# PERFORMANCE OF LINUX

## 1.1 Python script check Linux

### How to run

```bash
# Configuration
Create .env and configure according to .env.example

# Install all packages
pip install python-dotenv psutil pyinstaller

# Build
pyinstaller --onefile src/main.py

# Run
./dist/main
```

## 2.1 Service management

```bash

# Create file service in /etc/systemd/system
# Add scripts as linuxhealth.service in file above
# Note: Remember to change path of project in option: ExecStart
sudo nano /etc/systemd/system/linuxhealth.service

# Reload the Systemd daemon
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable linuxhealth.service 

# Start service
sudo systemctl start linuxhealth.service

# Check status. If everything is correct, it will be active
sudo systemctl status linuxhealth.service

```

## 2.2 Crontab

```bash

```

## 2.3 Build file DEB

[Download here](https://github.com/HoangAnh-it/linux-performance/blob/main/debian_package/linuxhealthdeb.deb)

```bash
# Install package
sudo dpkg -i linuxhealthdeb.deb

# Start service
sudo systemctl start linuxhealth.service

# Check status to make sure that linuxhealth service is active
sudo systemctl status linuxhealth.service

# More
# Configure linuxhealth service
# Restart service after making any changes
Go into /etc/linuxhealth/linuxhealth.properties

```
## 3. Docker

```bash
docker-compose up -d
docker-compose down
```
