# DB-project

#Duck Tours App

A user-friendly tours application that allows users to book services, including yacht trips, safaris, and aqua park visits, based on various filters. The app also provides an admin interface for managing services and viewing transactions.

 Features
- User interface for browsing and booking services.
- Admin interface to manage services, categories, and view transactions.
- Service filtering by capacity and price.
- Email tickets sent to users upon successful booking.
- Dynamic category creation for services if a new category is added.

Tech Stack
- Python: Programming language used for the application.
- Tkinter: GUI framework for building the user and admin interfaces.
- Pillow: For image processing and displaying images in the app.
- MySQL: Database for storing user, service, category, and transaction data.
- SMTP: Email functionality for sending tickets to users.
- tkcalendar: For implementing a calendar widget.

 Installation Instructions

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/shrooq-hussien/DB-project.git
   ```

2. Navigate to the project directory:
   ```bash
   cd DB-project
   ```

3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MySQL database using the schema provided.

5. Run the app:
   ```bash
   python main.py
   ```

6. Follow the on-screen instructions to interact with the app.

 Database Setup

1. Import the following schema into your MySQL database:
   ```sql
 
    CREATE DATABASE  DuckDB;
    USE DuckDB;


   CREATE TABLE Category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) UNIQUE NOT NULL
   );


    CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(11) NOT NULL,
    CONSTRAINT Email_Format CHECK (Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT Phone_Format CHECK (PhoneNumber REGEXP '^[0-9]{11}$')
    );


   CREATE TABLE Admin (
    NationalID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(11) NOT NULL,
    CONSTRAINT Admin_Email_Format CHECK (Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT Admin_Phone_Format CHECK (PhoneNumber REGEXP '^[0-9]{11}$')
       );


    CREATE TABLE Service (
      ServiceID INT AUTO_INCREMENT PRIMARY KEY,
      Name VARCHAR(100) NOT NULL,
      CategoryID INT NOT NULL,
      Price DECIMAL(10, 2) NOT NULL,
      Location VARCHAR(255),
      ImagePath VARCHAR(255),
      OwnerID INT,
      Capacity INT NOT NULL DEFAULT 0,
      FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
      FOREIGN KEY (OwnerID) REFERENCES Admin(NationalID)
     );


   CREATE TABLE Transaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ServiceID INT NOT NULL,
    TransactionDate DATE NOT NULL,
    TicketDate DATE NOT NULL,
    NumberOfPeople INT NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
    );

   DELIMITER $$

   CREATE TRIGGER CalculateTotalAmount
    BEFORE INSERT ON Transaction
    FOR EACH ROW
    BEGIN
       DECLARE servicePrice DECIMAL(10, 2);
       SELECT Price INTO servicePrice FROM Service WHERE ServiceID = NEW.ServiceID;
       SET NEW.TotalAmount = servicePrice * NEW.NumberOfPeople;
   END$$

   DELIMITER ;


   INSERT INTO Category (Name)
    VALUES 
    ('Yacht'),
    ('Safari'),
    ('Aqua Park');


    INSERT INTO Admin (NationalID, Name, Email, PhoneNumber)
    VALUES 
       (1001, 'Admin One', 'admin1@gmail.com', '01234567890'),
       (1002, 'Admin Two', 'admin2@gmail.com', '09876543210');


   INSERT INTO Service (Name, CategoryID, Price, Location, ImagePath, OwnerID)
   VALUES
      ('Luxury Yacht', 1, 1000.00, 'Marsa Matrouh Marina', 'yacht1.jpg', 1001,250),
      ('Speedboat Adventure', 1, 800.00, 'Marsa Matrouh Marina', 'speedboat.jpg', 1002,150),
      ('Desert Safari', 2, 500.00, 'Marsa Matrouh Desert', 'safari.jpg', 1001,1000),
      ('Water Slide', 3, 200.00, 'Aqua Fun Park', 'slide.jpg', 1002,500),
      ('Wave Pool', 3, 300.00, 'Aqua Fun Park', 'wavepool.jpg', 1001,700);


   INSERT INTO User (Name, Email, PhoneNumber)
    VALUES
       ('Shrooq Hussien', 'Shohussien37@icloud.com', '01234567890'),
       ('Nada', 'Nada37@icloud.com', '09876543210');


   INSERT INTO Transaction (UserID, ServiceID, TransactionDate, TicketDate, NumberOfPeople)
      VALUES
    (1, 1, '2024-12-01', '2024-12-10', 4),
    (2, 2, '2024-12-02', '2024-12-15', 3),
    (1, 3, '2024-12-03', '2024-12-20', 5);
    
  





   ```
the schema is ![Schemafinal drawio](https://github.com/user-attachments/assets/a9ff0d75-6361-4d73-bece-dc11c37476b6)
 Usage

- service provider interface: Admins can add, edit, and delete services, manage categories, and view transactions.
- User interface: Users can browse categories, filter services by price and capacity, book services, and receive an email ticket with the booking details.




 **`requirements.txt`**

```txt
Pillow
mysql-connector
tkcalendar
```

This `requirements.txt` includes the external libraries your project depends on. If you already have these installed, users can install all the necessary dependencies by running:

```bash
pip install -r requirements.txt
```


