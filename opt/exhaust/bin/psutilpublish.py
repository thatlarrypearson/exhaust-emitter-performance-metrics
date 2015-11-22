#!/usr/bin/python
#
# psutilpublish.py
#
# Description:
#
# Arguments:
#	 See Environment Variables for AMQP connection information.
#    See "available_calls" dictionary
#
# Environment Varaibles:
# - AMQP Connection Information:
#
# Dependencies:
#	- pika==0.10.0
#	- sarge==0.1.4
#   - psutil==3.2.1
#
# Published Data Format:
#   {
#      "TAGS":".source.s_psutil",
#      "SOURCEIP":"127.0.0.1",
#      "PROGRAM":"psutilpublish",
#      "PRIORITY":"info",
#      "MESSAGE":"<acct-record>",
#      "LEGACY_MSGHDR":"psutil: ",
#      "HOST_FROM":"<hostname>",
#      "HOST":"<hostname>",
#      "FACILITY":"daemon",
#      "DATE":"<date>"
#      "UTC-TIMESTAMP":"<utc-timestamp>"
#   }
#
# Usage:
#	accttail | acctpublish.py
#
# See Also:
#	- accttail.c
#	- syslogtopic.py
__author__ = 'lbp'

import pika
import json
import sys
import os
import datetime
import time
import psutil

from sarge import get_stdout

def psutil_disk_usage():
    rtnVal = []
    disks = psutil.disk_partitions(all=True)
    for disk in disks:
        rtnVal.append(psutil.disk_usage(disk[1]))
    return rtnVal

def psutil_process_iter():
    rtnVal = []
    for proc in psutil.process_iter():
        rtnVal.append(proc.as_dict())
    return rtnVal

settings = {}

defaults = {
    "pikahost":                   "localhost",
    "pikaport":                   5672,
    "pikavirtual-host":           None,
    "pikausername":               "guest",
    "pikapassword":               "guest",
    "pikachannel-max":            None,
    "pikaframe-max":              None,
    "pikaheartbeat-interval":     None,
    "pikassl":                    None,
    "pikassl-options":            None,
    "pikaconnection-attempts":    32768,
    "pikaretry-delay":            5,
    "pikasocket-timeout":         5,
    "pikalocale":                 None,
    "pikabackpressure-detection": None,
    "while-loop-delay-in-seconds": 600,
    "for-loop-delay-in-seconds":   1,
    }

available_calls = {
    "psutil.cpu_times": {
        "obj": psutil.cpu_times,
        "args": [],
        "kwargs": {
            "percpu": False,
        },
    },
    "psutil.cpu_percent": {
        "obj": psutil.cpu_percent,
        "args": [],
        "kwargs": {
            "percpu": True,
            "interval": None,
        },
    },
    "psutil.cpu_count": {
        "obj": psutil.cpu_count,
        "args": [],
        "kwargs": {
            "logical": False,
        },
    },
    "psutil.logical_cpu_count": {
        "obj": psutil.cpu_count,
        "args": [],
        "kwargs": {
            "logical": False,
        },
    },
    "psutil.virtual_memory": {
        "obj": psutil.virtual_memory,
        "args": [],
        "kwargs": {}
    },
    "psutil.swap_memory": {
        "obj": psutil.swap_memory,
        "args": [],
        "kwargs": {}
    },
    "psutil.disk_partitions": {
        "obj": psutil.disk_partitions,
        "args": [],
        "kwargs": {
            "all": True,
        }
    },
    "psutil.disk_usage": {
        "obj": psutil_disk_usage,
        "args": [],
        "kwargs": {}
    },
    "psutil.disk_io_counters": {
        "obj": psutil.disk_io_counters,
        "args": [],
        "kwargs": {
            "perdisk": True,
        }
    },
    "psutil.net_io_counters": {
        "obj": psutil.net_io_counters,
        "args": [],
        "kwargs": {
            "pernic": True,
        }
    },
    "psutil.net_if_addrs": {
        "obj": psutil.net_if_addrs,
        "args": [],
        "kwargs": {}
    },
    "psutil.net_if_stats": {
        "obj": psutil.net_if_stats,
        "args": [],
        "kwargs": {}
    },
    "psutil.users": {
        "obj": psutil.users,
        "args": [],
        "kwargs": {}
    },
    "psutil.boot_time": {
        "obj": psutil.boot_time,
        "args": [],
        "kwargs": {}
    },
    "psutil.process_iter": {
        "obj": psutil_process_iter,
        "args": [],
        "kwargs": {}
    },

}

calllist = []
for key, value in available_calls.items():
    calllist.append(key)

def hostname():
    s = get_stdout("hostname")
    # print "hostname=%s" % (s.strip(), )
    return s.strip()

def ipaddress():
    s = get_stdout("hostname -I")
    a = s.split()
    # print "ipaddress=%s" % (a[0], )
    return a[0]

def environmentvariable(name):
    if name in os.environ:
        return os.environ[name]
    elif name in defaults:
        return defaults[name]
    else:
        return None

def nixtime2utc(str):
    t = datetime.datetime.utcfromtimestamp(int(str))
    return t.isoformat()

settings["pikahost"]                   = environmentvariable("pikahost")
settings["pikaport"]                   = int(environmentvariable("pikaport"))
settings["pikavirtual-host"]           = environmentvariable("pikavirtual-host")
settings["pikausername"]               = environmentvariable("pikausername")
settings["pikapassword"]               = environmentvariable("pikapassword")
settings["pikachannel-max"]            = environmentvariable("pikachannel-max")
settings["pikaframe-max"]              = environmentvariable("pikaframe-max")
settings["pikaheartbeat-interval"]     = environmentvariable("pikaheartbeat-interval")
settings["pikassl"]                    = environmentvariable("pikassl")
settings["pikassl-options"]            = environmentvariable("pikassl-options")
settings["pikaconnection-attempts"]    = environmentvariable("pikaconnection-attempts")
settings["pikaretry-delay"]            = environmentvariable("pikaretry-delay")
settings["pikasocket-timeout"]         = environmentvariable("pikasocket-timeout")
settings["pikalocale"]                 = environmentvariable("pikalocale")
settings["pikabackpressure-detection"] = environmentvariable("pikabackpressure-detection")

settings["while-loop-delay-in-seconds"] = environmentvariable("while-loop-delay-in-seconds")
settings["for-loop-delay-in-seconds"]   = environmentvariable("for-loop-delay-in-seconds")

settings["ipaddress"] = ipaddress()
settings["hostname"] = hostname()

# connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672/%2F'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings["pikahost"],
        port=settings["pikaport"],
        virtual_host=settings["pikavirtual-host"],
        credentials = pika.credentials.PlainCredentials(
             username=settings["pikausername"], password=settings["pikapassword"]
        ),
        channel_max=settings["pikachannel-max"],
        frame_max=settings["pikaframe-max"],
        heartbeat_interval=settings["pikaheartbeat-interval"],
        ssl=settings["pikassl"],
        ssl_options=settings["pikassl-options"],
        connection_attempts=settings["pikaconnection-attempts"],
        retry_delay=settings["pikaretry-delay"],
        socket_timeout=settings["pikasocket-timeout"],
        locale=settings["pikalocale"],
        backpressure_detection=settings["pikabackpressure-detection"]
    ))

channel = connection.channel()

while True:
    for call in calllist:
        utc_ts = datetime.datetime.utcnow()
        local_datetime = datetime.datetime.now()

        #
        #  psutil calls go here...
        #
        objcall = available_calls[call]["obj"]
        args = available_calls[call]["args"]
        kwargs = available_calls[call]["kwargs"]
        message = objcall(*args, **kwargs)

        publish_message = {
            "TAGS":              ".source.s_psutil",
            "SOURCEIP":          settings["ipaddress"],
            "PROGRAM":           "psutilpublish",
            "PRIORITY":          "info",

            "MESSAGE": {
                call: message,
            },

            "LEGACY_MSGHDR":     "psutil: ",
            "HOST_FROM":         settings["hostname"],
            "HOST":              settings["hostname"],
            "FACILITY":          "daemon",
            "DATE":              local_datetime.strftime("%b %e %H:%M:%S"),
            "UTC-TIMESTAMP":     utc_ts.isoformat(),
        }

        channel.basic_publish(
            'syslog',
            'syslog',
            json.dumps(publish_message),
            pika.BasicProperties(content_type="application/json", delivery_mode=1)
        )
        time.sleep(settings["for-loop-delay-in-seconds"])
    time.sleep(settings["while-loop-delay-in-seconds"])

connection.close()
