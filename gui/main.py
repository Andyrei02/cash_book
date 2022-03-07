import sys
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets

from .gui import Ui_CashBook
from .file_manage import FileWR
from .db_manage import DataBaseWR



class App(Ui_CashBook):
	def __init__(self):
		self.file_w_r = FileWR()
		self.db = DataBaseWR()
		self.translate = QtCore.QCoreApplication.translate
		self.money = str
		self.amount_text_var = None
		self.page_selected = str

	def create_new_entries(self, description: str, balance_event: int, 
									balance: int, time_date: str, in_or_out: str):
		description = str(description)
		balance_event = str(balance_event)
		balance = str(balance)
		time_date = str(time_date)

		self.frame_second = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.frame_second.setMinimumSize(QtCore.QSize(500, 170))
		self.frame_second.setMaximumSize(QtCore.QSize(16777215, 170))
		self.frame_second.setStyleSheet("background-color: rgb(209, 209, 209);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 10px;\n"
"border-color:  rgb(150, 150, 150);\n"
"min-width: 10em;\n"
"padding: 6px;")
		self.frame_second.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame_second.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame_second.setObjectName("frame_second")
		self.gridLayout = QtWidgets.QGridLayout(self.frame_second)
		self.gridLayout.setObjectName("gridLayout")
		self.description_label = QtWidgets.QLabel(self.frame_second)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.description_label.setFont(font)
		self.description_label.setStyleSheet("background-color: rgb(202, 202, 202);\n"
"border-style: intset;\n"
"border-width: 2px;\n"
"border-radius: 10px;\n"
"border-color:  rgb(150, 150, 150);\n"
"min-width: 10em;\n"
"padding: 6px;")
		self.description_label.setAlignment(QtCore.Qt.AlignCenter)
		self.description_label.setObjectName("description_label")
		self.gridLayout.addWidget(self.description_label, 0, 0, 3, 1)
		self.event_label = QtWidgets.QLabel(self.frame_second)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		self.event_label.setFont(font)
		self.event_label.setAlignment(QtCore.Qt.AlignCenter)
		self.event_label.setObjectName("event_label")
		self.gridLayout.addWidget(self.event_label, 0, 2, 1, 1)
		self.balance_label = QtWidgets.QLabel(self.frame_second)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		self.balance_label.setFont(font)
		self.balance_label.setAlignment(QtCore.Qt.AlignCenter)
		self.balance_label.setObjectName("balance_label")
		self.gridLayout.addWidget(self.balance_label, 1, 1, 1, 1)
		self.total_balance = QtWidgets.QLabel(self.frame_second)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		self.total_balance.setFont(font)
		self.total_balance.setAlignment(QtCore.Qt.AlignCenter)
		self.total_balance.setObjectName("total_balance_1")
		self.gridLayout.addWidget(self.total_balance, 1, 2, 1, 1)
		self.time_label = QtWidgets.QLabel(self.frame_second)
		self.time_label.setAlignment(QtCore.Qt.AlignCenter)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.time_label.setFont(font)
		self.time_label.setObjectName("time_label")
		self.gridLayout.addWidget(self.time_label, 2, 1, 1, 2)
		self.verticalLayout_5.addWidget(self.frame_second)

		if in_or_out == 'cash_in':
			self.event_label.setStyleSheet("color: green;")
		elif in_or_out == 'cash_out':
			self.event_label.setStyleSheet("color: red;")

		self.description_label.setText(self.translate("CashBook", description))
		self.balance_label.setText(self.translate("CashBook", "Balance"))
		self.total_balance.setText(self.translate("CashBook", balance))
		self.event_label.setText(self.translate("CashBook", balance_event))
		self.time_label.setText(self.translate("CashBook", time_date))

	def get_current_time(self):
		time = datetime.datetime.now()
		date = time.strftime("%d-%B-%Y")
		hour = time.strftime("%H:%M %p")
		return [str(date), str(hour)]

	def click_cash_in(self):
		self.page_selected = "in"
		self.stackedWidget.setCurrentIndex(1)

	def click_cash_out(self):
		self.page_selected = "out"
		self.stackedWidget.setCurrentIndex(1)

	def cancel_event(self):
		self.amount_text.clear()
		self.amount_text.setStyleSheet("")
		self.remark_text.clear()
		self.page_selected = 0
		self.stackedWidget.setCurrentIndex(self.page_selected)

	def save_event(self):
		amount_text_var = self.amount_text.toPlainText()
		remark_text_var = self.remark_text.toPlainText()
		self.amount_text.clear()
		self.remark_text.clear()

		list_time = self.get_current_time()

		try:
			amount_text_var = float(amount_text_var)
		except ValueError:
			self.amount_text.setStyleSheet("border: 1px solid red;")
		else:
			self.amount_text.setStyleSheet("")

			if self.page_selected == "in":
				self.create_new_entries(remark_text_var, amount_text_var,
										self.money, "  ".join(list_time), 'cash_in')
				self.money = self.money + amount_text_var
				self.db.write_in_db((list_time[0], list_time[1], str(remark_text_var), amount_text_var, 0, self.money))


			elif self.page_selected == "out":
				self.create_new_entries(remark_text_var, amount_text_var, 
										self.money, "  ".join(list_time), 'cash_out')
				self.money = self.money - amount_text_var
				self.db.write_in_db((list_time[0], list_time[1], str(remark_text_var), 0, amount_text_var, self.money))
			self.curent_balance.setText(self.translate("CashBook", str(self.money)))
			
			self.file_w_r.write('money.txt', self.money)
			self.stackedWidget.setCurrentIndex(0)

	def main(self):
		self.cash_in_btn.clicked.connect(self.click_cash_in)
		self.cash_out_btn.clicked.connect(self.click_cash_out)
		self.cancel_btn.clicked.connect(self.cancel_event)
		self.save_btn.clicked.connect(self.save_event)

		self.updade_entries()

	def updade_entries(self):
		self.money = int(self.file_w_r.read('money.txt'))
		self.curent_balance.setText(self.translate("CashBook", str(self.money)))

	def run(self):
		app = QtWidgets.QApplication(sys.argv)
		window = QtWidgets.QMainWindow()
		self.setupUi(window)
		self.main()
		window.show()
		sys.exit(app.exec_())
