# Documentation for Django Application: Personal Trust

### Project Setup

1. Ensure that you have docker, docker-compose
2. Clone the existing repository
3. Start up the application
```bash
sudo docker-compose up -d
```
4. Run migrations
```bash
sudo docker-compose exec project_web python manage.py migrate
```
5. Create superuser
```bash
sudo docker-compose exec project_web python manage.py createsuperuser
```

# Documentation for Django Application: Personal Trust

## Overview

The Personal Trust application is designed to manage client information, addresses, and relationships. This application was developed focusing on user authentication, client management, and relationship handling. The project includes a robust backend with Django and a responsive frontend using Bootstrap. Unit and functional tests have been written for each implemented user story to ensure reliability and correctness.

## Achievements

### Authentication
1. **User Login**:
   - Implemented a login page with a custom design for user authentication.
   - Navbar shows login status (e.g., "Logged in as Joe Soap" for authenticated users).
   - Login button is visible only to non-authenticated users.
   - Functional tests ensure non-authenticated users can log in and authenticated users can see their status.

2. **User Logout (Bonus)**:
   - Implemented a logout functionality.
   - Logout button is visible only to authenticated users.
   - Functional tests ensure authenticated users can log out successfully.

### Clients
1. **Access Control**:
   - Non-authenticated users cannot access the client list.
   - Navbar hides the client list button for non-authenticated users.
   - Functional tests ensure proper access control and visibility based on authentication status.

2. **Client List Pagination**:
   - Client list is paginated to show only 20 clients per page.
   - Pagination controls allow navigation to the first, last, previous, and next pages.
   - Functional tests ensure the pagination works correctly and displays the appropriate number of clients per page.

3. **Client Search**:
   - Basic search bar above the client list allows filtering by name, surname, or ID number.
   - (Real-time search is currently under development)
   - Functional tests ensure the search functionality works correctly and updates the client list as expected.

4. **Client Creation**:
   - Client creation form allows adding new clients with their details and addresses.
   - Validates South African ID numbers using the Luhn algorithm.
   - Ensures uniqueness of ID numbers in the database.
   - Functional tests ensure the client creation form validates inputs correctly and handles duplicate ID numbers appropriately.

### Address Management
- **Address Form**:
  - Fields for street, city, province, postal code, country, and address type.
  - Linked with the client creation form to capture address information during client registration.
  - Functional tests ensure addresses are correctly associated with clients and validated.

### Frontend Design
- **Home Page**:
  - Redesigned with a modern and engaging layout.

- **Login Page**:
  - Enhanced visual appeal with a creative and user-friendly design.

## Not Achieved (Under Development)
1. **Client Relationship Management**:
   - Logic for creating and managing client relationships is present but currently breaking.
   - Ensuring inverse relationships are created simultaneously.
   - Requires further debugging and testing to ensure stability and correctness.

2. **Real-time Search**:
   - Real-time search functionality for the client list is not currently operational.
   - Requires additional development and testing to ensure smooth real-time updates.

3. **Visual Feedback for Duplicate ID Numbers**:
   - Currently, there is no visual feedback on the client creation form for ensuring the uniqueness of ID numbers.
   - Users need clear error messages and feedback when attempting to input duplicate ID numbers.

### Future Work
1. **Fix Client Relationship Management**:
   - Debug and fix the breaking issues in the client relationship logic.
   - Ensure that inverse relationships are correctly created and managed.

2. **Implement Real-time Search**:
   - Complete the development and integration of real-time search functionality for the client list.

3. **Improve Error Handling**:
   - Add comprehensive error messages and user feedback for different scenarios, especially for duplicate ID numbers.

4. **Refactoring**:
   - Refactor existing code to improve readability, maintainability, and performance, ensuring adherence to best practices and design patterns.

### Conclusion
The Personal Trust application has made significant progress in managing client and address information, with a robust user authentication system and a user-friendly frontend design. The application’s primary functionalities are in place, but further development and debugging are required to fully achieve all planned features, particularly the client relationship management and comprehensive error handling.
