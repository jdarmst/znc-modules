#!/usr/bin/python
# noticetoquery.py
# Convert /notice's from services to /msg's since some networks won't load "nickserv/set_privmsg"
# Credits: " KindOne " for the idea and initial base.

import znc

class noticetoquery(znc.Module):
    description = "Makes services /notice's look like a /msg."
# Make module only load at network level for now.
    module_types = [znc.CModInfo.NetworkModule]

    def OnLoad (self,args,message):
        self.nv['n'] = "nickserv chanserv botserv helpserv operserv hostserv"
        self.nv['p'] = "^"
        return True
    
    def OnPrivNotice(self, nick, msg):
        if nick.GetNick().lower() in self.nv['n'].split():
            self.PutUser(":"+self.nv['p']+nick.GetHostMask()+" PRIVMSG "+self.GetUser().GetNick()+" :(notice) "+msg.s)
            return znc.HALTCORE
        return znc.CONTINUE
        
    def OnUserMsg(self, target, message):
        self.PutModule(target.s[0])
        if target.s[0] == self.nv['p']:
            self.PutModule("Target matches prefix")
            if target.s[1:].lower() in self.nv['n'].split():
                self.PutModule("target is in the list")
                self.PutIRC("PRIVMSG "+target.s[1:]+" :"+message.s)
                znc.HALTCORE
    
    def OnModCommand(self, command):
        list = self.nv['n'].split()
        word = command.split()
        com = word[0].lower()
        if com == "list":
            self.PutModule("Current nicks:")
            self.PutModule("    "+str(list))
        elif com == "prefix":
            try:
                type(word[1])
                # There was an argument passed
                
                # check the length
                if len(word[1]) > 1:
                    self.PutModule("Only one character, please!")
                elif word[1] in ['@','!','~']:
                    self.PutModule("I can't let you do that!")
                else:
                    # We're good!
                    self.nv['p'] = word[1]
                    self.PutModule("Prefix set")
            except:
                self.PutModule("Current prefix: "+self.nv['p'])
        elif com == "help":
            self.PutModule("Commands:\n\n\
    Add    :   Add a nick to redirect\n\
    Del    :   Stop redirecting that nick\n\
    Prefix :   Set/Get prefix character for private messages\n\
    List   :   List redirected nicks\n\
    Help   :   Display this help list")
        elif com not in ['add','del']:
            self.PutModule("unknown command")
        else:
            try:
                type(word[1])
            except:
                self.PutModule("Please provide an argument!")
            if com == "del":
                try:
                    list.remove(word[1].lower())
                    self.PutModule("Removed")
                except:
                    self.PutModule("Not in list")
                    return znc.CONTINUE
            elif com == "add":
                try:
                    list.index(word[1].lower())
                    self.PutModule("Already in list")
                    return znc.CONTINUE
                except:
                    list.append(word[1].lower())
                    self.PutModule("Added")
        self.nv['n'] = " ".join(list)
