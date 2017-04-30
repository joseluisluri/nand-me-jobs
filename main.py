#!/usr/bin/env python3
from status import status
from datomatic import parse

def print_menu():
    print(30 * "-" , "JOBS" , 30 * "-")
    print("1. Update status")
    print("2. Parse DATS in datomatic dir")
    print("3. Exit")
    print(67 * "-")

loop=True
while loop:
    print_menu()
    choice = input("Enter your choice [1-3]: ")

    # Update status
    if choice == '1':
        status.do()
    elif choice == '2':
        parse.do()
    elif choice == '3':
        loop = False
        continue
    else:
        print('Wrong option selection.')

    input('Enter any key to try again..')
