import json
import streamlit as st

# Set Background Image

import streamlit as st

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* For tablets and smaller laptops (max-width: 1024px) */
        @media (max-width: 1024px) {{
            .stApp {{
                background-size: cover;
                background-position: center;
            }}
        }}

        /* For mobile devices (max-width: 768px) */
        @media (max-width: 768px) {{
            .stApp {{
                background-size: contain;
                background-position: top center;
                background-attachment: scroll;
            }}
        }}

        /* For very small screens (max-width: 480px) */
        @media (max-width: 480px) {{
            .stApp {{
                background-size: cover;
                background-position: center;
                background-attachment: scroll;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set Background Image (Online Image or Local File)
set_background("https://www.shutterstock.com/image-photo/book-open-pages-close-up-600nw-2467818435.jpg")  # Use an online book-themed image


# Storage File
STORAGE_FILE = "books_data.json"

# Load Books from File
def load_books():
    try:
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save Books to File
def save_books(books):
    with open(STORAGE_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Initialize Book Collection
books = load_books()

# Streamlit UI
st.title("📚 Book Collection Manager")

# Navigation Sidebar
menu = st.sidebar.radio("Navigate", ["Add Book", "View Books", "Search Books", "Update Book", "Remove Book", "Reading Progress"])

# Add New Book
if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Book Title:")
    author = st.text_input("Author:")
    year = st.text_input("Publication Year:")
    genre = st.text_input("Genre:")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        books.append(new_book)
        save_books(books)
        st.success(f'📖 "{title}" has been added!')

# View All Books
elif menu == "View Books":
    st.header("📚 Your Book Collection")
    if books:
        for book in books:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("No books in your collection.")

# Search Books
elif menu == "Search Books":
    st.header("🔎 Search Books")
    search_query = st.text_input("Search by Title or Author:")
    if st.button("Search"):
        results = [book for book in books if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

# Update Book
elif menu == "Update Book":
    st.header("✏ Update a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a Book to Update", book_titles)

    if selected_book:
        book = next((b for b in books if b["title"] == selected_book), None)
        new_title = st.text_input("New Title", book["title"])
        new_author = st.text_input("New Author", book["author"])
        new_year = st.text_input("New Year", book["year"])
        new_genre = st.text_input("New Genre", book["genre"])
        new_read = st.checkbox("Mark as Read", book["read"])

        if st.button("Update Book"):
            book.update({"title": new_title, "author": new_author, "year": new_year, "genre": new_genre, "read": new_read})
            save_books(books)
            st.success(f'✅ "{new_title}" updated successfully!')

# Remove Book
elif menu == "Remove Book":
    st.header("🗑 Remove a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a Book to Remove", book_titles)

    if selected_book and st.button("Remove Book"):
        books = [b for b in books if b["title"] != selected_book]
        save_books(books)
        st.success(f'🗑 "{selected_book}" removed successfully!')

# Reading Progress
elif menu == "Reading Progress":
    st.header("📊 Reading Progress")
    total_books = len(books)
    read_books = sum(1 for book in books if book["read"])
    progress = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"📖 Books Read: {read_books}")
    st.progress(progress / 100)
