from sqlCalls import isbnExist, lendStatus, lendBook, returnBook
import sqlCalls, apiCalls

def Main():
    while(True):
        isbn = input("What isbn would you like to check?\n")  # need to implement error checking for isbn
        if isbn != "db": ## type 'db' when the prototype askes for an isbn to show all db data
            if isbnExist(isbn): # tests if the book exists in the db
                status = lendStatus(isbn) # finds the status of the book being lent out
                title = sqlCalls.getBookInfo(isbn)[3]
                if status[0] == 0:
                    yn = input('Are you lending out ' + title + 'y/n\n')
                    if yn == "y":
                        name = input("To whom are you lending it to?\n")
                        lendBook(isbn, name)
                else:
                    print(status[1] + ' has this book')
                    yn = input('Are you getting this book back? y/n\n')
                    if yn == "y":
                        returnBook(isbn)
            else:
                apiCalls.getBook(isbn)
        else:
            sqlCalls.PrintDB()


Main()