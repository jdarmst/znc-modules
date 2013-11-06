# Allows second user to execute commands in a shell environment on the ZNC host machine
# This module is one of my bot modules, which means I use it with a separate connection
# to an IRC server than the one I use.

# Usage: $ <command>

#!/usr/bin/python
# comshell.py

import znc
import subprocess
import re
import os

class comshell(znc.Module):

    # hostmask must be a regex pattern
    hostmask = "ALLOWED HOSTMASK HERE"

    description = "Implements $ <command> shell in channels and query"
    module_types = [znc.CModInfo.NetworkModule]
    
    def OnChanMsg(self, nick, channel, message):
        global hostmask
        msg = message.s
        if msg[:2] == "$ ":
            host = nick.GetHostMask()
            pattern = re.compile(hostmask,re.I)
            m = pattern.match(host)
            if m:
                com = msg[2:]
                p = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
                i = 0
                for line in iter(p.stdout.readline,''):
                    i += 1
                    out = str(line)[2:-3]
                    if i > 10: break
                    if not out: break
                    self.PutIRC("PRIVMSG "+channel.GetName()+" :> "+out)
                if i > 10:
                    self.PutIRC("PRIVMSG "+channel.GetName()+" :Too much to send!")
                    os.killpg( p.pid,signal.SIGINT)
