public class Book {
    private int id;
    private String title;
    private String author;
    private boolean available;
    private String borrowerId;

    public Book(int id, String title, String author, boolean available, String borrowerId) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.available = available;
        this.borrowerId = borrowerId;
    }

    // Getters and Setters
    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public boolean isAvailable() { return available; }
    public String getBorrowerId() { return borrowerId; }

    public void setTitle(String title) { this.title = title; }
    public void setAuthor(String author) { this.author = author; }
    public void setAvailable(boolean status) { this.available = status; }
    public void setBorrowerId(String userId) { this.borrowerId = userId; }
}