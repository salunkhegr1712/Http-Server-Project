#basic code to open the web browser
import os 
import webbrowser

os.system('python server.py start')
webbrowser.open_new_tab("http://127.0.0.1:30000/index1.html")
os.system('python server.py stop')



# os.system()

