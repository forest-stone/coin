import threading
from .views import return24Volume

t = threading.Thread(target=return24Volume)
t.start()
