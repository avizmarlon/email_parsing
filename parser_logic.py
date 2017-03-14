import re
import os
from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askdirectory
import time

# todo:
# make renaming temporary, file names go back to their original after the parsing computation is done
# or find a way to parse without needing to rename (probably using regex).

rootWindow = Tk().withdraw()
folder = askdirectory(title="Choose the folder in which the .eml files are located") + "/"
mail_data = {}

# rename
print("Renaming folders...")
file_count = 0
folders = os.listdir(folder)
for file in folders:
	if str(file_count) + ".eml" in folders:
		file_count += 1
		continue
	os.rename(folder + file, str(file_count) + ".eml")
	file_count += 1


# parsing
for dirpath, dirname, filename in os.walk(folder):
	for file in filename:
		file_data = open(folder + file, "r")
		try:
			for line in file_data:
				line = line.rstrip()
				email_parsed = re.findall("^From: .* <(\S+)>", line)
				if len(email_parsed) > 0:
					email = email_parsed[0]
					print("Email found:", email)
					mail_data[email] = mail_data.get(email, 0) + 1
		except UnicodeDecodeError:
			continue


# show results sorted by number of ocurrences
# transforms dict into a list of tuples, inverts (key, val) for (val, key) and sorts it reversely
print("\nTake a look at the results:\n")
inversed_dict = [(count, email) for email, count in mail_data.items()]
for count, email in sorted(inversed_dict, reverse=True):
	print("Email:", email)
	print("Count:", count)
	print("\n")

# user interaction for filtering by keyword
while True:
	user_filter = input("Type a keyword and I will see what I can find. Type quit to, well... quit:\n")
	if user_filter == 'quit':
		print("Bye!")
		break
	print("The chosen keyword was:", user_filter, "\n")

	found_keyword_results = []
	for email, count in mail_data.items():
		if user_filter in email:
			found_keyword_results.append((count, email))

	if len(found_keyword_results) == 0:
		print("Nothing was found!\n")
		continue
	else:
		print("Found something!\n")
		for count, email in sorted(found_keyword_results, reverse=True):
			print("Email", email)
			print("Count", count)
			print("\n")
