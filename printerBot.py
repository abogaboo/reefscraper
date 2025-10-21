import openpyxl

wBook = openpyxl.load_workbook("repo.xlsx")
sheet = wBook.active

name = input("input name\n")
number = input("input number\n")
epa = input("input epa\n")
data = [name, number, epa]

sheet.append(data)
wBook.save("repo.xlsx")
print("done!")
