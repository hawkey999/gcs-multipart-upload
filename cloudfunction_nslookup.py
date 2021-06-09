import socket


def getaddrinfo(request):
  ip_list = []
  ais = socket.getaddrinfo("storage.googleapis.com",0,0,0,0)
  for result in ais:
    ip_list.append(result[-1][0])
  print(str(ip_list))
  return str(ip_list)
