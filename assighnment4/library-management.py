import json

class Library:
    def __init__(self):
        self.books = []
        self.file_name = "library.json"
        self.load_library()

    def load_library(self):
        try:
            with open(self.file_name, "r") as file:
                self.books = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_library(self):
        with open(self.file_name, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self):
        title = input("Enter the book title: ")
        author = input("Enter the author: ")
        year = input("Enter the publication year: ")
        genre = input("Enter the genre: ")
        read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        self.books.append({
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status
        })
        self.save_library()
        print("Book added successfully!\n")

    def remove_book(self):
        title = input("Enter the title of the book to remove: ")
        for book in self.books:
            if book["title"].lower() == title.lower():
                self.books.remove(book)
                self.save_library()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    def search_book(self):
        choice = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        keyword = input("Enter search keyword: ").lower()
        found_books = [book for book in self.books if keyword in book["title"].lower() or keyword in book["author"].lower()]

        if found_books:
            print("Matching Books:")
            for idx, book in enumerate(found_books, 1):
                read_status = "Read" if book["read"] else "Unread"
                print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        else:
            print("No matching books found.")
        print()

    def display_books(self):
        if not self.books:
            print("Your library is empty!\n")
            return

        print("Your Library:")
        for idx, book in enumerate(self.books, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        print()

    def display_statistics(self):
        total_books = len(self.books)
        if total_books == 0:
            print("No books in the library.\n")
            return

        read_books = sum(1 for book in self.books if book["read"])
        percentage_read = (read_books / total_books) * 100
        print(f"Total books: {total_books}")
        print(f"Percentage read: {percentage_read:.2f}%\n")

    def run(self):
        while True:
            print("Menu\nWelcome to your Personal Library Manager!")
            print("1. Add a book")
            print("2. Remove a book")
            print("3. Search for a book")
            print("4. Display all books")
            print("5. Display statistics")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.display_books()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                self.save_library()
                print("Library saved to file. Goodbye!")
                break
            else:
                print("Invalid choice, please try again!\n")

if __name__ == "__main__":
    Library().run()
