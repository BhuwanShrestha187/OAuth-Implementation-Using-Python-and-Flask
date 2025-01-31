<h1> About the Project</h1>
This project is made for learning basic Web Building with Flask and Python using OAuthentication for authentication purposes. 

<h2>This project is intended to meet these kind of requirements: </h2>
<ul>
  <h3>
  <li>Flask Integration</li>
  <li>Use Python</li>
  <li>Use OAuthentication</li>
  <li>Implement SQL Server for checking the user already has account or not.</li>
  <li>Creating a new user account</li>
  <li>Forgot Password Functionality</li>
  </h3>
</ul>

<h2>Progress Made so far:</h2>
<ul>
  <h3>
  <li>First Sprint: Flask Integration with Python and Basic UI structure is completed as of Jan 31, 2025</li>
  </h3> 
  <h3><li>Second Sprint: Adding the verifying username and password Functionality with SQL Server database: </h3></li>
  <p>In the second sprint, I utlized the integration of checking if the credentials entered by the user match the credentials stored in my local database in SQL Server. Right now, I did not implemented any password hashing. 
  I manually entered a test user in the database, and checked it in the web application. Flask try to compare the password using <b>check_password_hash()</b> function but I temporarily disabled it using <b>if user_data[3] == password:
  </b>.  </p>
</ul>
