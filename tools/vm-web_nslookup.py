import socket
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def getaddrinfo():
  ip_list = []
  ais = socket.getaddrinfo("storage.googleapis.com",0,0,0,0)
  for result in ais:
    ip_list.append(result[-1][0])
  print(str(ip_list))
  return str(ip_list)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 80)))