import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time

#Update Rent,Pumping Charges,Account Id,RR number and Contact Details here
###########################################################################################
FH_Rent = #Rent Amount
OH_Rent = #Rent Amount
Pumping_charges = #Pumping Charges
FH_account_id = #RR Number
OH_account_id = #RR Number
RR_id_number = #Water Bill Number
FH_contact_number =   #Contact Number Tenant
OH_contact_number =   #Contact Number Tenant
self_contact_number = #Self Contact Number
############################################################################################
#Update Rent,Pumping Charges,Account Id,RR number and Contact Details here

#Way2SMS API for sending SMS
############################################################################################
def sendPostRequest_FH(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
	  req_params = {
	  'apikey':'XXXXXXXXXXXXXX', #Your Way2SMS API Key
	  'secret':'XXXXXXXXXXXXXX', #Your Way2SMS API Secrect
   	  'usetype':'prod',
	  'phone': FH_contact_number,
	  'message': FH_message,
	  'senderid':'XXXXX' #Your Way2SMS Sender ID
	  }
	  return requests.post(reqUrl, req_params)
############################################################################################

#Chrome Driver and URL details
chromedriver = "XXX" #Path for Chrome driver
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chromedriver,chrome_options=options)
delay = 20
URL = 'http://www.way2sms.com/api/v1/sendCampaign'


#Front House electricity Bill
def main():
	try:
		driver.get("https://bescom.org/pay-bill/")
		FH_acc_id = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="accno"]')))
		FH_acc_id.send_keys(FH_account_id)
		FH_submit = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit3"]')))
		FH_submit.click()
	except TimeoutException:
		print ("Loading took too much time!")

	try:
		electricity_month_text = datetime.now().strftime('%h')
		FH_bill_month = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ctl00_MasterPageContentPlaceHolder_MasterPageContentPlaceHolder_lblDueDateValue"]'))).text
		if(FH_bill_month != 'NA'):
			FH_bill_month_split = FH_bill_month.split('-')[1]
			if(electricity_month_text == FH_bill_month_split):
				FH_amount = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ctl00_MasterPageContentPlaceHolder_MasterPageContentPlaceHolder_txtAmounttoPay"]')))
				FH_value = FH_amount.get_attribute('value')
				if(FH_value != 0):
					print('Outstanding Front House Electricity Bill Amount = ' + str(FH_value))
				else:
					print('Front House Electricity Bill Amount already paid')
			else:
				FH_value = 0
				print('Month is different, No value considered')
		else:
			FH_value = 0
			print('Front House Electricity Bill Amount already paid')
	except TimeoutException:
	    print ("Loading took too much time!")

	#Outhouse electricity Bill
	try:
		driver.get("https://bescom.org/pay-bill/")
		OH_acc_id = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="accno"]')))
		OH_acc_id.send_keys(OH_account_id)
		OH_submit = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit3"]')))
		OH_submit.click()
	except TimeoutException:
	    print ("Loading took too much time!")

	try:
		electricity_month_text = datetime.now().strftime('%h')
		OH_bill_month = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ctl00_MasterPageContentPlaceHolder_MasterPageContentPlaceHolder_lblDueDateValue"]'))).text
		if(OH_bill_month != 'NA'):
			OH_bill_month_split = OH_bill_month.split('-')[1]
			if(electricity_month_text == OH_bill_month_split):
				OH_amount = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ctl00_MasterPageContentPlaceHolder_MasterPageContentPlaceHolder_txtAmounttoPay"]')))
				OH_value = OH_amount.get_attribute('value')
				if(OH_value != 0):
					print('\n!-----------!\n')
					print('Outstanding Out House Electricity Bill Amount = ' + str(OH_value))
				else:
					print('Out House Electricity Bill Amount already paid')
			else:
				OH_value = 0
				print('Month is different, No value considered')
		else:
			OH_value = 0
			print('Out House Electricity Bill Amount already paid')
	except TimeoutException:
	    print ("Loading took too much time!")

	#Water Bill Details
	driver.get("https://www.bwssb.gov.in/login")
	try:
		electricity_month_num = datetime.now().strftime('%m')
		Quick_pay = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div[2]/a')))
		window_before = driver.window_handles[0]
		Quick_pay.click()
		time.sleep(5)
		window_after = driver.window_handles[1]
		driver.switch_to_window(window_after)
		rr_id = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_txtrrnumber"]')))
		rr_id.send_keys(RR_id_number)
		rr_id.send_keys(u'\ue007')
		rr_bill_month_id = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_txtbilldate"]')))
		rr_bill_month = rr_bill_month_id.get_attribute('value').split('/')[1]
		if(int(rr_bill_month) == int(electricity_month_num)-1):
			rr_bill_value_id = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_txtAmount"]')))
			rr_bill_value = rr_bill_value_id.get_attribute('value')
			if(rr_bill_value != 0):
				print('Outstanding Water Bill = ' + rr_bill_value)
			else:
				print('Water Bill already paid')
		else:
			print('Month is different, No value considered')
	except TimeoutException:
	    print ("Loading took too much time!")
	driver.close()
	driver.switch_to_window(window_before)
	driver.close()

	print('\n!-----------!\n')
	Ind_water_bill = round(int(rr_bill_value)/3)
	print('Individual Water Bill = ' + str(Ind_water_bill))
	print('Outstanding Front House electricity Bill = ' + str(FH_value))
	print('Outstanding Out House electricity Bill = ' + str(OH_value))

	FH_total_bill = FH_Rent+int(FH_value)+Ind_water_bill+Pumping_charges
	OH_total_bill = OH_Rent+int(OH_value)+Ind_water_bill+Pumping_charges

	print('\n!-----------!\n')
	print('Front House Total Bill = ' + str(FH_total_bill))
	print('Out House Total Bill = ' + str(OH_total_bill))

	print('\n!-----------!\n')
	print('Please check the below details carefully\n')
	print('Front House Rent Details')
	FH_message_prepare = ('Hi \nGreetings \nPFB the Rent Details for ' + str(electricity_month_text) + '\n Rent: ' + str(FH_Rent) + '\n Water Bill: ' + str(Ind_water_bill) + '\n Electricity Bill: ' + str(FH_value) + '\n Pumping: ' + str(Pumping_charges) + '\n Total: ' + str(FH_total_bill))
	FH_message = FH_message_prepare + '\nThanks \n XXX'
	print(FH_message)

	print('\n!-----------!\n')
	print('\n\nOut House Rent Details')
	OH_message_prepare = ('Hi \nGreetings \nPFB the Rent Details for ' + str(electricity_month_text) + '\n Rent: ' + str(OH_Rent) + '\n Water Bill: ' + str(Ind_water_bill) + '\n Electricity Bill: ' + str(OH_value) + '\n Pumping: ' + str(Pumping_charges) + '\n Total: ' + str(OH_total_bill))
	OH_message = OH_message_prepare + '\nThanks \n XXX'
	print(OH_message)

	print('\n!-----------!\n')
	sms_response = input('Do you wish to send SMS? Enter (Y/N): ')
	if(sms_response == 'Y' or sms_response == 'y'):
		sendPostRequest_FH(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage) #Enter all Details here for Tenant 1
		sendPostRequest_FH(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage) #Enter all Details here for Tenant 2
		sendPostRequest_FH(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage) #Enter all Details here for Self(To maintain records)
	else:
		print('\n!-----------!\n')
		print('\nThank you, If details are found to be incorrect please run program again in a few days\n')

if __name__ == '__main__':
	main()















