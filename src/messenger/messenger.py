"""
File contains the global message mechanism for Scrib
"""

from model.model import SCR_Base_List


"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Messenger():

    messages = SCR_Base_List()

    def __init__(self):

        pass

    def create_message(self,message_name):

        _message = SCR_Message(message_name)

        self.messages.add(_message)

    def publish(self,message_name,data):

        _message = self.messages.find_by_attribute("name",message_name)

        if _message != None:

            _message.publish(data)

    def subscribe(self,message_name,callout):

        _message = self.messages.find_by_attribute("name",message_name)

        if _message != None:

            _message.add_subscriber(callout)

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):
        
        _txt  = ""

        for _message in self.messages:

            _txt += "{}\n".format(str(_message))

        return _txt

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Message():

    def __init__(self,name):

        self.name        = name
        self.subscribers = SCR_Base_List()

    def add_subscriber(self,callout):

        _subscriber = SCR_Messenger_Subscriber()

        _subscriber.callout = callout

        self.subscribers.add(_subscriber)

    def publish(self,data):

        for _subscriber in self.subscribers:

            if _subscriber.callout != None:

                _subscriber.callout(data)

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):
        
        _txt  = "Message [{}] \n".format(self.name)

        for _subscriber in self.subscribers:

            _txt += "{}\n".format(str(_subscriber))

        return _txt

"""******************************************************************************************
*********************************************************************************************
******************************************************************************************"""
class SCR_Messenger_Subscriber():

    def __init__(self):

        self.callout = None

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):
        
        _txt = "    Subscriber [{}]".format(self.name, self.callout)

        return _txt