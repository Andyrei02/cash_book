
# start qt-tools: pyqt5-tools designer
import os

# print('Convert ui to py...')

# os.system('pyuic5 D:\\Project\\python\\cash_book\\gui\\qt-gui\\form.ui -o D:\\Project\\python\\cash_book\\gui\\gui.py')

from gui.main import App

# print('Convert complete.\nStarting app')

app = App()
app.run()
