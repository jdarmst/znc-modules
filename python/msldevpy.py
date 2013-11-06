#!/usr/bin/python

# My first python module for ZNC, so -shrug-
# Gets information for a mantis bug report and
# displays it in the channel. This is for a ZNC
# based bot, so it would have it's own connection.

# USAGE: #<ticket number>

import re
from urllib.request import urlopen
import znc

class msldevpy(znc.Module):
    description = "Python bot"
    
    def OnChanMsg(self, nick, chan, msg):
        if chan.GetName().lower() == "#msldev":
            m = re.match("^#(\d+)$", msg.s)
            if m:
                num = str(m.group(1))
                num = num.lstrip("0")
                if num == "":
                    return znc.CONTINUE
                page = urlopen("http://localhost/getmSLDevData.php?id="+num)
                mydata = page.read()
                mydata = str(mydata)[2:-1]
                if not re.match("\[ Information Unavailable \]",mydata):
                	line = "Issue #"+num+": [ http://www.msldev.com/bugs/view.php?id="+num+" ] "+mydata
                else:
                	line = "Issue #"+num+" does not exist!"
                self.PutIRC("PRIVMSG "+chan.GetName()+" :"+line)
                self.PutUser(":myResponse!me@SavageCL.com PRIVMSG "+chan.GetName()+" :"+line)

        return znc.CONTINUE
