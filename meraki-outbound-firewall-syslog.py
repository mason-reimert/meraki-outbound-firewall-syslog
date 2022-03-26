HOST, PORT = "0.0.0.0", 514

import socketserver
import matplotlib.pyplot as plt
from datetime import date

firewalls = {}
today = date.today()


def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

def log(port,IP):
	if IP in firewalls:
		if port in firewalls[IP]:
			firewalls[IP][port] = firewalls[IP][port] + 1
		else:
			firewalls[IP][port] = 1
	else:
		firewalls[IP] = {}
		firewalls[IP][port] = 1

class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]

		Port = find_between(str(data),"dport="," ")
		IP = self.client_address[0]

		log(Port,IP)
        

if __name__ == "__main__":
	try:
		server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		left = []
		height = []
		tick_label = []

		for firewall in firewalls:
			for port in firewalls[firewall]:
				tick_label.append(port)
				left.append(len(left)+1)
				
			for count in firewalls[firewall].values():
				height.append(count)
	
			plt.bar(left, height, tick_label = tick_label, width = 0.8, color = ['red', 'green'])
			
			# naming the x-axis
			plt.xlabel('Outbound Ports')
			# naming the y-axis
			plt.ylabel('Hit Count')
			# plot title
			plt.title(firewall + ' Outbound Ports Graph')
			
			# function to show the plot
			plt.savefig(firewall +'.png')
			plt.show()
			print(firewalls)
			print ("Crtl+C Pressed. Shutting down.")