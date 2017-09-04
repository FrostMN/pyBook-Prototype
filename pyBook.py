from sqlCalls import isbnExist, lendStatus, lendBook, returnBook, addBook
import sqlCalls, apiCalls, valid

def Main():
    while(True):
        isbn = getISBN() #input("Please enter an ISBN, 'db', or 'q':\n")  # need to implement error checking for isbn
        if isbn != "db" and isbn != "q": ## type 'db' when the prototype askes for an isbn to show all db data or 'q' to quit I know this isnt the best way but its there for now
            if isbnExist(isbn): # tests if the book exists in the db
                status = lendStatus(isbn) # finds the status of the book being lent out
                title = sqlCalls.getBookInfo(isbn)[3]
                if status[0] == 0:
                    yn = input('Are you lending out \'' + title + '\'? y/n\n')
                    if yn == "y":
                        name = input("To whom are you lending it to?\n")
                        lendBook(isbn, name)
                else:
                    print(status[1] + ' has this book')
                    yn = input('Are you getting this book back? y/n\n')
                    if yn == "y":
                        returnBook(isbn)
            else:
                newBook = apiCalls.getBook(isbn)
                yn = input('Are you adding \'' + newBook._title + '\' to your library? y/n\n')
                if yn == "y":
                    addBook(newBook)
        elif isbn == "q":
            break
        else:
            sqlCalls.PrintDB()
    print("Thanks for using the pyBook-Prototype!")


def getISBN():
    while True:
        inPut = input("Please enter an ISBN, 'db', or 'q':\n")
        if inPut == 'db' or inPut == 'q':
            return inPut
        isbn = valid.ISBN(inPut)
        if isbn != False:
            return isbn



Main()