# Exhaust Emitter - Performance Metrics

Performance metrics is one type of exhaust emitter, a component of the [Exhaust Proof-of-Concept](https://github.com/ThatLarryPearson/exhaust-PoC).

Peformance metrics takes advantage of the [psutil](https://github.com/giampaolo/psutil) Python library.  The `psutil` library is able to interrogate the operating system and return performance metrics into the calling environment provided by the included Pyhon program.

## Installation

Make sure that the software can find the RabbitMQ server.  As a precondition, you should already have installed the [collector](https://github.com/ThatLarryPearson/exhaust-collector).  In one of the collector install steps had you get the IP address of the server by issuing the `hostname -I` command.  You need the IP address from that command to use when modifying the the `/etc/hosts` file.
```
sudo su - root
echo '<IP Address from RabbitMQ Host>' rabbitmq >> /etc/hosts
exit
```

Python libraries to install:
- [psutil](https://github.com/giampaolo/psutil) [docs](https://pythonhosted.org/psutil/)
- [pika](https://github.com/pika/pika) [docs](https://pika.readthedocs.org/en/latest/index.html)
- [sarge](https://github.com/vsajip/sarge) [docs](http://sarge.readthedocs.org/en/latest/)

Install Python `pip` and Python libraries:
```
sudo apt-get install -y python-pip
sudo -H pip install --upgrade pip
sudo pip install psutil pika sarge
```

Use `git` to fetch the necessary files.
```
sudo apt-get install git-core
git clone https://github.com/ThatLarryPearson/exhaust-emitter-performance-metrics.git
cd exhaust-emitter-performance-metrics
sudo mkdir --parents /opt/exhaust/bin /opt/exhaust/etc
sudo cp opt/exhaust/bin/psutilpublish.py /opt/exhaust/bin
sudo cp opt/exhaust/bin/syslogtopic.py /opt/exhaust/bin
sudo cp opt/exhaust/bin/installservice.sh /opt/exhaust/bin
sudo cp opt/exhaust/etc/exhaust.conf /opt/exhaust/etc
sudo cp etc/init/psutilpublish.conf /etc/init
sudo chown -R root:root /opt/exhaust/bin/*
sudo chown root:root /etc/init/psutilpublish.conf
sudo chmod 0755 /opt/exhaust /opt/exhaust/* /opt/exhaust/bin/*
sudo chmod 0644 /opt/exhaust/etc/*
sudo chmod 0644 /etc/init/psutilpublish.conf
sudo /opt/exhaust/bin/installservice.sh
service --status-all
service psutilpublish restart
```

To test, run the `syslogtopic.py` command and you should see all of the messages flowing into the message queue:
```
/opt/exhaust/bin/syslogtopic.py
```

## Licensing

The MIT License (MIT)

Copyright &copy; 2015 Lawrence Bennett Pearson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




