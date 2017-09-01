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
      Book_ID int AUTO_INCREMENT,
      isbn10 int,
      isbn13 int,
      title varchar(200),
      status int,
      lendee varchar(200),
      PRIMARY KEY (Book_ID)
      )
    """)

    ## Loads in test Data for development
    c.execute("""    
    INSERT INTO books (Book_ID, isbn10, isbn13, title, status, lendee) VALUES ('1', '0380973464', '9780380973460', 'Cryptonomicon', 0, "" );
              """)
    c.execute("""
    INSERT INTO books (Book_ID, isbn10, isbn13, title, status, lendee) VALUES ('2', '0380973123', '0380973464123', 'Cryptonomicron', 1, "Amber" );
              """)

    ## commits changes and closes the connection
    conn.commit()
    conn.close()


def PrintDB():
    ## prints all data from the db

    conn = sqlite3.connect('pyBook.db')
    c = conn.cursor()
    sql_res = c.execute("select * from books")
    print(sql_res.fetchall())
    conn.commit()
    conn.close()


def Execute(call, params=None):
    ## exectues a sql query, currenly ony does single query, but will be extended to do multiple
    if params == None:
        conn = sqlite3.connect('pybook.db')
        c = conn.cursor()
        c.execute(call)
        conn.commit()
        conn.close()


def isbnExist(isbn):
    ## queries the db to determine if a book has an entry
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    if len(isbn) == 13:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn13=' + isbn)
    else:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn10=' + isbn)
    count = c.fetchone()
    conn.commit()
    conn.close()
    if count[0] == 0:
        return False
    else:
        return True


def lendStatus(isbn):
    conn = sqlite3.connect('pybook.db')
    c = conn.cursor()
    if len(isbn) == 13:
        c.execute('SELECT status, lendee FROM books WHERE isbn13=' + isbn)
    else:
        c.execute('SELECT status, lendee FROM books WHERE isbn10=' + isbn)
    status = c.fetchone()
    conn.commit()
    conn.close()
    return status


def lendBook(isbn, lendee):
    if len(isbn) == 13:
        call = "UPDATE books SET status='1', lendee='{{lendee}}' WHERE isbn13=" + isbn
    else:
        call = "UPDATE books SET status='1', lendee='{{lendee}}' WHERE isbn10=" + isbn

    call = call.replace("{{lendee}}", lendee)
    Execute(call)
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()


def returnBook(isbn):
    # builds the correct string depending on which isbn is used
    if len(isbn) == 13:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn13=" + isbn
    else:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn10=" + isbn
    Execute(call) # runs the update call to "return" the book
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()
