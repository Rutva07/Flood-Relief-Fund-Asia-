# Flood Relief Fund(Asia)
#### Video Demo:  https://youtu.be/qQF76fsK2mQ
#### Description: This website is designed using flask, bootstrap, jinja, sqlite, javascript, css, html and python, and it helps people who don't have enough financial support and are affected by flood in Asia
My project contains a python file named app.py, a static folder that contains images and styles.css that contains design for website, requirements.txt for knowing which external function app.py uses, database.db that stores information, flood.csv that stores natural disaster events of year 2023, README.md that contains information of my project and templates folder stores all .html files.

My project is a website designed to help poor people in Asia who have lost their home or have no money for basic amenities due to the outrage of flood. In the present year 2023, many Asian countries have suffered due to flood and my project will serve as a medium to help those people affected by flood.

Flood Relief Fund(Asia) is a simple website that lets anyone in the world donate any amount for the sake of those affected by flood and lets people of certain countries withdraw money. Certain countries include those Asian countries which are affected by flood. First, any donor or person who needs money needs to 'register' and subsequently 'log in' to the website to avail the facilities.

Four databases namely donors, receivers, available and users are used to store details of users according to their action. Their registration is stored in database users. Users that donate any amount are added to database donors and users who withdraw fund are added to database receivers. Available database stores total fund available and it is updated everytime when anyone donates or withdraws money.

The user who is a donor needs to simply enter username, amount(no limit) and card details to donate. Donors must use Visa or MasterCard to donate. Their entered card details will be checked. People who needs the raised fund must enter their country, username, passport number and amount they require(limit $500). If user falls in flood affected Asian country, then only they will be able to withdraw fund. Passport numbers will be used by the website to ensure that user is certified.

Moreover, the website also displays top donors' person_id and the amount they donated. Their name is not shown due to privacy purposes. Fund available for users to withdraw is also shown, so that they can see how much fund is left. All data such as registration, donor and its details, fund receiver and its details are stored in databases.

## How to Start the Application
1. Clone the repository: git clone https://github.com/Rutva07/Flood-Relief-Fund-Asia
2. Navigate to the project directory: cd Flood-Relief-Fund-Asia (or folder name if changed) 
3. Run the Flask application in terminal: flask run
4. Navigate to given address.

## File Information

### Flask app (app.py)
This is the main application file containing the Flask server setup, routes, and message handling logic.

### HTML Templates (templates/...)
These are the template files that defines the structure and style of the web pages. It includes input forms for posting messages, a button to submit messages, a section to display messages, links, images and many more.

### CSS Styles (static/styles.css | templates/all files)
This includes simple styles to enhance the visual appearance of the message blocks, form elements and other html elements.

### CSV File (flood.csv)
Contains information related to flood activities in year 2023.

### Database File (database.db)
Holds information of users, donations, withdrawl requests, etc.





