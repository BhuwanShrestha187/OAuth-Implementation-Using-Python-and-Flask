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
  <ul>
    <li>Under the second sprint, finished the Incorrect Password Functionality!!!</li>
  </ul>
  <li><h3>Third Sprint: Forgot Password Functionality:</h3></li>
  <p>Successfully integrated the forgot password functionality. But there is one glitch still need to be fixed. When user successfully changed the password and then try to login
  with the new password, it successfully gets login. And when user press the Log out button from the dashboard page, then it came back to the homepage, but the problem happening is
  that, in  the login UI, it is displaying "Login Successful" which is previous result, right. So when user presses Log Out, he should be given new window of login page which 
  should be completely clean.</p>

  <p>So, to solve that issue, I need to clear the session may be in the Logout route!!</p>
</ul>
