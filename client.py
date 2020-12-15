import enet

host = enet.Host(enet.Address("188.27.45.124", 54301), 1, 0, 0, 0)
peer = host.connect(enet.Address("82.76.59.55", 54301), 1)

while 1:
    event = host.service(1000)
    if event.type == enet.EVENT_TYPE_CONNECT:
        print("%s: CONNECT" % event.peer.address)
        break