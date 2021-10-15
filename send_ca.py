#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging, sys
from getpass import getpass
from argparse import ArgumentParser
from common_class import my_sql
import slixmpp

#For mysql password
sys.path.append('/var/gmcs_config')
import astm_var

send_to_examination_id=1006

class SendMsgBot(slixmpp.ClientXMPP):

    """
    A basic Slixmpp bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        await self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect()


if __name__ == '__main__':
    # Setup logging.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    m=my_sql()
    con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
    cur=m.run_query(con,'select * from im_message where message_status=0',());
    dt=m.get_single_row(cur);
    while(dt):
      print(dt)
      xmpp = SendMsgBot(astm_var.xmpp_user, astm_var.xmpp_pass, dt[1], '{}'.format(dt[2]))
      xmpp.register_plugin('xep_0030') # Service Discovery
      xmpp.register_plugin('xep_0199') # XMPP Ping

      # Connect to the XMPP server and start processing XMPP stanzas.
      xmpp.connect()
      xmpp.process(forever=False)

      update_cur=m.run_query(con,'update im_message set message_status=1 where id=%s',(dt[0],))
      dt=m.get_single_row(cur);


    m.close_cursor(cur)
    m.close_link(con)
