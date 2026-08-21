# Tech University API

Description: Application Programming Interface (API) for Tech University

Tech University is a full-stack web application where students can sign up for courses.  There is an Application Programming Interface (API) component that interacts with a SQL database and handles authentications and authorizations.  There is also a User Interface (UI) component.  You can check out the UI component via this [link](https://github.com/vstarr-tkh/tech-university-ui).  Session cookies are used to authenticate users.  JSON is the data format used for transferring data between the UI and the API.  The end points for the API are:

- /users/{userId}
    - End point for fetching user profile images
- /students
    - End point for fetching students enrolled at Tech University
- /courses
    - End point for fetching courses taught at Tech University
- /faculty
    - End point for fetching faculty who teach at Tech University
- /enrollments
    - End point for fetching student enrollments for courses and creating  enrollments for courses
- /enrollments/{studentId}
    - End point for fetching enrollments for student with id `studentId`
- /login
    - Endpoint for logging in a user
- /logout
    - Endpoint for logging out a user
- /session
    - Endpoint for getting user session