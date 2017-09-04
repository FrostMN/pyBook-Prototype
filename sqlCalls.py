import sqlite3

## All sql function in this file need to be reworked to use proper parameter substitution to prevent injection
## I currently just have it 'working' and will look at security later

def CreateDB():
    ## creates the connection to the sqlite db
    conn = sqlite3.connect('pyBook.db')
    c = conn.cursor()

    ## String to build the db for the application
    c.execute("""
    CREATE TABLE books(
      Book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
      isbn10 int,
      isbn13 int,
      title varchar(200),
      author_ln varchar(200),
      author_fn varchar(200),
      status int,
      lendee varchar(200)
      );
    """)

    ## commits changes and closes the connection
    conn.commit()
    conn.close()


def PrintDB():
    ## prints all data from the db

    conn = sqlite3.connect('pyBook.db')
    c = conn.cursor()
    sql_res = c.execute("select * from books")

    print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")
    print("| " + "Book_id".ljust(7) + " | " + "isbn10".ljust(10) + " | " + "isbn13".ljust(13) + " | " + "title".ljust(40) + " | " + "author_ln".ljust(15) + " | " + "author_fn".ljust(15) + " | status | " + "lendee".ljust(20) + " |")
    print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")
    for entry in sql_res.fetchall():
        print("| " + str(entry[0]).rjust(7) + " | " + str(entry[1]).rjust(10, "0") + " | " + str(entry[2]) + " | " + str(entry[3][0:40]).ljust(40) + " | " + str(entry[4]).ljust(15) + " | " + str(entry[5]).ljust(15) + " | " + str(entry[6]).rjust(6) + " | " + str(entry[7]).ljust(20) + " |")
        print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")
    conn.commit()
    conn.close()


def Execute(call, params=None):
    ## exectues a sql query
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    if params == None:
        c.execute(call)
    else:
        c.execute(call, params)
    conn.commit()
    conn.close()



def isbnExist(isbn):
    ## queries the db to determine if a book has an entry
    param = (isbn,)
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    if len(isbn) == 13:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn13=?', param)
    else:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn10=?', param)
    count = c.fetchone()
    conn.commit()
    conn.close()
    if count[0] == 0:
        return False
    else:
        return True


def lendStatus(isbn):
    param = (isbn,)
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    # builds the correct string depending on which isbn is used
    if len(isbn) == 13:
        c.execute('SELECT status, lendee FROM books WHERE isbn13=?', param)
    else:
        c.execute('SELECT status, lendee FROM books WHERE isbn10=?', param)
    status = c.fetchone()
    conn.commit()
    conn.close()
    return status


def lendBook(isbn, lendee):
    params = (lendee, isbn)

    # builds the correct string depending on which isbn is used
    if len(isbn) == 13:
        call = "UPDATE books SET status='1', lendee=? WHERE isbn13=?"
    else:
        call = "UPDATE books SET status='1', lendee=? WHERE isbn10=?"
    Execute(call, params)
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()


def returnBook(isbn): ##
    # builds the correct string depending on which isbn is used
    params = (isbn,)
    if len(isbn) == 13:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn13=?"
    else:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn10=?"
    Execute(call, params) # runs the update call to "return" the book
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()


def Fetch(call, params): ## returns a line from the db will change to make more universal
    param = (params,)
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    c.execute(call, param)
    fetched = c.fetchone()
    conn.commit()
    conn.close()
    return fetched



def getBookInfo(isbn):  ## should change this to return a book object from sql call
    if len(isbn) == 13:
        call = "SELECT * FROM books WHERE isbn13=?"
    else:
        call = "SELECT * FROM books WHERE isbn10=?"
    return Fetch(call, isbn)

def addBook(book):
    call = """
INSERT INTO books(isbn10, isbn13, title, author_ln, author_fn, status, lendee) 
VALUES( ?, ?, ?, ?, ?, 0, '');
"""
    call_params = ( book._isbn10, book._isbn13, book._title, book._author_ln, book._author_fn )
    Execute(call, call_params)