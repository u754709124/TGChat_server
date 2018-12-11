import datetime
import hashlib

m=hashlib.sha1()
strs = "40bd001563085fc35165329ea1ff5c5ecbdbbeef" + "fq2Y6YQv6LxH8rb3"
m.update(strs.encode("utf8"))
print(m.hexdigest())
