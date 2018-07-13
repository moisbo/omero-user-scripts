#!/usr/bin/env python
import omero
from omero.gateway import BlitzGateway
from Parse_OMERO_Properties import USERNAME, PASSWORD, HOST, PORT

conn = BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT)

if conn.connect():

    user = conn.getUser()
    print "Current user:"
    print "   ID:", user.getId()
    print "   Username:", user.getName()
    print "   Full Name:", user.getFullName()

else:
    print "cannot connect"
