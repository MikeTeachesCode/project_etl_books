import csv, os, sqlite3
FOLDER = "DATA"
data_curr = [] ### CURRENT_AUTHORS_BOOKS.CSV
data_legacy = [] ### LEGACY_AUTHORS_BOOKS.CSV
### EXTRACT DATA
def extract():
    ### CURRENT AUTHORS
    with open(FOLDER + os.sep +\
              "current_authors_books.csv", "r") as file:
        reading = csv.DictReader(file)
        for row in reading:
            data_curr.append({
                "author_id": row["id"],
                "author": row["Author Name"],
                "title": row["Book Title"],
                "price": float(row["Price (GBP)"]),
            })
    ### LEGACY AUTHORS
    with open(FOLDER + os.sep +\
              "legacy_authors_books.csv", "r") as file:
        reading = csv.DictReader(file)
        for row in reading:
            data_legacy.append({
                "author_id": row["id"],
                "author": row["Author Name"],
                "title": row["Book Title"],
                "price": float(row["Price (GBP)"]),
            })

### TRANSFORM DATA
def transform():
    [data_curr[i].update({"type": "current"})
        for i in range(len(data_curr))]

    [data_legacy[i].update({"type": "legacy"})
        for i in range(len(data_legacy))]

    combined_data = data_curr + data_legacy
    
    return combined_data


### LOAD DATA
def load():
    combined_data = transform()
    ### CREATE BOOKS TABLE
    conn = sqlite3.connect("bookstore.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books(
        id INTEGER PRIMARY KEY,
        author TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        title TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        type TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES Authors(id)
    )
    """)
    
    ### INSERT DATA INTO BOOKS TABLE
    for book in combined_data: ### LIST OF DICTIONARIES
        cursor.execute("""
        INSERT INTO Books (author, author_id, title, price, type)
        VALUES (?, ?, ?, ?, ?)
        """, (book["author"], int(book["author_id"]),
              book["title"], float(book["price"]), 
             book["type"]
             ))
    conn.commit()
    conn.close()
    
    print("Inserted data into Books table. ETL process completed")
    
def main():
    extract()
    load()
    
if __name__ == "__main__":
    main()