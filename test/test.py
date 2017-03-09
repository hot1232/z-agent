import gevent

def t1():
    while True:
        print("hello")
        gevent.sleep(1)
        pass;



g1=gevent.spawn(t1)
g1.start()
gevent.joinall([g1])
print("over")
while True:
    pass;

print(over)