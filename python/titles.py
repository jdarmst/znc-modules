#!/usr/bin/python
# page title reader

# Simple, sometimes ineffective title reader.
# This is a bot module, meaning it gets it's own
# connection, along with the other bot modules!

import re
from urllib.request import urlopen
import znc

class titles(znc.Module):
    description = "Read titles"
    
    def OnChanMsg(self, nick, chan, msg):
        m = re.search("(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)", msg.s)
        if m:
            url = str(m.group(1))
            page = urlopen(url)
            c = re.compile("<title>(.*?)</title>")
            for line in page:
                trial = c.search(str(line))
                if trial:
                    self.PutIRC("PRIVMSG "+chan.GetName()+" :[ Title : "+str(trial.group(1))+" ] [ URL: "+url+" ]")
                    break
            page.close()
        return znc.CONTINUE
