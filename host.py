import enet

host = enet.Host(enet.Address(b"localhost", 54301), 10, 0, 0, 0)
print(enet.Address(b"localhost", 54301))

while 1:
    # Wait 1 second for an event
    event = host.service(0)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: CONNECT" % event.peer.address)
        break