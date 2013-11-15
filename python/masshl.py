# mass highlight kicker
# masshl.py
# Credit to " KindOne " for the idea.

import znc
import re

class masshl(znc.Module):
    
    def OnLoad(self, args, message):
        self.nv['chans'] = ""
        self.nv['limit'] = "4"
        self.nv['type'] = "0"
        self.nv['ban'] = "no"
        self.nv['message'] = "Mass Highlighting is not permitted!"
        return True
    
    def storeList(self, list):
        self.nv['chans'] = " ".join(list)
        return True
    
    def getList(self):
        return self.nv['chans'].split()
    
    def OnChanMsg(self, nick, channel, message):
        mymodes = channel.GetPermStr()
        m = re.compile("[~&@%]")
        if m.search(mymodes):
            # we can kick and ban, so let's have at it!
            
            # make list of nicks in channel
            nicks = channel.GetNicks()
            names = []
            for n in nicks:
                names.append(re.escape(n.lower()))
            m = re.compile("("+"|".join(names)+")")
            c = m.findall(" ".join(set(message.s.lower().split())))
            if len(c) > int(self.nv['limit']):
                if self.nv['type'] == "1":
                    # We're being exclusive
                    if channel.GetName().lower() in self.getList(): return znc.CONTINUE
                else:
                    # We're being inclusive
                    if channel.GetName().lower() not in self.getList(): return znc.CONTINUE
                
                # Example of a raw kickban
                # MODE #Jordan +b *!*KindOne@*.wwbnc.com
                # KICK #Jordan kindone
                self.PutModule("Taking action (ban="+self.nv['ban']+") against "+nick.GetNick()+" for highlighting "+str(len(c))+" people in "+channel.GetName())
                if self.nv['ban'] == "yes": self.PutIRC("MODE "+channel.GetName()+" +b "+"*!*@"+nick.GetHost())
                self.PutIRC("KICK "+channel.GetName()+" "+nick.GetNick()+" "+self.nv['message'])

    
    def OnModCommand(self, command):
        list = self.getList()
        word = command.split()
        com = word[0].lower()
        
        if com == "help":
            self.PutModule("Commands:\n\n\
    limit     :  Set/get allowed amount of highlights in a line (kickban if over)\n\
    type      :  Set/get how the channel list works (inclusive/exclusive)\n\
    ban       :  Set/get whether we ban (yes/no)\n\
    message   :  Set/get the kick message\n\
    list      :  Print a list of the current channels\n\
    add       :  Add a channel to the list\n\
    del       :  Delete a channel from the list\n\
    help      :  Print this documentation")
        elif com == "type":
            try:
                type(word[1])
                # parameter exists
                if word[1] in ['1','0']:
                    self.nv['type'] = word[1]
                    self.PutModule("set")
                else:
                    self.PutModule("accepted parameters:\n    1 : exclusive (don't kick in these channels)\n    2 : inclusive (only kick in these channels)")
            except:
                # parameter doesn't exist, print current type
                self.PutModule("Type: "+("1 : exclusive (don't kick in these channels)" if self.nv['type'] == "1" else "0 : inclusive (only kick in these channels)"))
        elif com == "ban":
            try:
                type(word[1])
                # parameter exists
                if word[1].lower() not in ['yes','no']:
                    self.PutModule("Yes or No, please")
                else:
                    self.nv['ban'] = word[1].lower()
                    self.PutModule("set")
            except:
                self.PutModule("We Ban? "+self.nv['ban'])
        elif com == "limit":
            try:
                type(word[1])
                # parameter exists
                try:
                    int(word[1])
                    # it's a number
                    self.nv['limit'] = str(word[1])
                    self.PutModule("set")
                except:
                    self.PutModule("Only numbers, please")
            except:
                # parameter doesn't exist: print current limit
                self.PutModule("Current limit: "+self.nv['limit'])
        elif com == "message":
            try:
                type(word[1])
                # there's a message
                self.nv['message'] = " ".join(word[1:])
                self.PutModule("set")
            except:
                self.PutModule("Current message:\n    "+self.nv['message'])
        elif com == "list":
            self.PutModule("Current channels:\n    "+(self.nv['chans'] if self.nv['chans'] != "" else "None set"))
        elif com not in ['add','del']: self.PutModule("Unknown command")
        else:
            try:
                type(word[1])
            except:
                self.PutModule("you must provide a channel!")
                return znc.CONTINUE
            list = self.getList()
            candidate = word[1].lower()
            if com == "add":
                try:
                    list.index(candidate)
                    # channel already in list
                    self.PutModule("Already in list")
                except:
                    # not currently in list
                    list.append(candidate)
                    self.storeList(list)
                    self.PutModule("Added")
            elif com == "del":
                try:
                    list.index(candidate)
                    # channel is in list
                    list.remove(candidate)
                    self.storeList(list)
                    self.PutModule("Deleted")
                except:
                    # channel not in list
                    self.PutModule("Channel not in list")
                    
