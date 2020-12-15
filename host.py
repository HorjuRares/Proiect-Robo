import enet

host = enet.Host(enet.Address("188.27.45.124", 54301), 10, 0, 0, 0)

while 1:
    # Wait 1 second for an event
    event = host.service(0)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: CONNECT" % event.peer.address)
        break