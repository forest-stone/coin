import threading
from .views import return24Volume

print("start")
t = threading.Thread(target=return24Volume)
t.start()
