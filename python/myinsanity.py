# !/usr/bin/python
# myinsanity.py

# I called this myinsanity because I wrote it for someone who's on > 60 networks...

# usage: /znc *myinsanity showme

# example output: I see 1000 people in 10 channels on 2 networks!"

import znc

class myinsanity(znc.Module):
    
    description = "How many people do I see?"
    module_types = [znc.CModInfo.UserModule]
    
    def OnModCommand(self, string):
        if string == "showme":
            self.PutModule("Command executed")
            # get networks and loop through them.
            c = 0
            u = 0
            n = 0
            for network in self.GetUser().GetNetworks():
                n += 1
                for channel in network.GetChans():
                    u += int(channel.GetNickCount())
                    c += 1
            self.PutModule("I see "+str(u)+" people in "+str(c)+" channels on "+str(n)+" networks!")
