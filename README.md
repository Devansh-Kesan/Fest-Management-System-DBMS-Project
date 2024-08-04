# Fest-Management-System-DBMS-Project

## About the Project (Website/App)

This project is a Fest Management System built using Flask, HTML, and CSS. It provides a basic UI/website for managing festival events.

## Project Structure:

The project is organized into the following main components:
1) static folder: Contains the CSS files for styling the website.
2) templates folder: Contains the HTML files for the various pages of the website.
3) newapp.py: Contains the main code to run the Flask application.

## How to Run the website:

To run the project, follow these steps:

1) Ensure you have Python and Flask installed on your system.
2) Copy newapp.py, the static folder, and the templates folder into a single directory.
3) Open Visual Studio Code (VS Code) and open the directory containing the files.
4) Click the Run button at the top of the VS Code interface to start the application.

The website will be hosted locally, and you can interact with it via your web browser.


**Introduction**

The Fest Management System is a comprehensive database designed to manage and organize festivals, their participants, events, sponsors, and various other related entities. This system ensures efficient handling of information and provides functionalities such as querying and reporting on different aspects of the festivals.

## Database Schema

![Copy of er diagram](https://github.com/user-attachments/assets/7e6b3e70-9123-4ef0-9cae-238f950bba2e)

### 1. FEST
- **Fest_id**: Primary key (int)
- **Name**: Name of the festival (varchar)
- **Start_date**: Date when the fest begins (date)
- **End_date**: Date when the fest ends (date)
- **Location_id**: Foreign key referencing the location where the fest takes place (int)
- **Organizer_id**: Foreign key referencing the organizer responsible for the fest (int)
- **Description**: Textual description of the fest (text)
- **Budget**: Budget allocated for the fest (decimal)

### 2. PARTICIPANT
- **Participant_id**: Primary key (int)
- **User_id**: Foreign key referencing the user associated with the participant (int)
- **Fest_id**: Foreign key referencing the fest in which the participant is registered (int)

### 3. VENUE
- **Venue_id**: Primary key (int)
- **Name**: Name of the venue (varchar)
- **Location_id**: Foreign key referencing the location of the venue (int)
- **Capacity**: Maximum capacity of the venue (int)
- **Description**: Description of the venue (text)

### 4. USER
- **User_id**: Primary key (int)
- **Username**: User’s username (varchar)
- **Email**: User’s email address (varchar)
- **Password**: User’s password (varchar)
- **First_name**: User’s first name (varchar)
- **Last_name**: User’s last name (varchar)
- **Phone_number**: User’s phone number (varchar)
- **Bio**: User’s biography (text)
- **Role_id**: Foreign key referencing the user’s role (int)

### 5. SPONSORSHIP
- **Sponsorship_id**: Primary key (int)
- **Fest_id**: Foreign key referencing the fest associated with the sponsorship (int)
- **Sponsor_id**: Foreign key referencing the sponsor providing the sponsorship (int)
- **Sponsor_level_id**: Foreign key referencing the sponsorship level (int)
- **Amount**: Monetary amount of the sponsorship (decimal)
- **Description**: Description of the sponsorship (text)

### 6. SPONSOR LEVEL
- **Sponsor_level_id**: Primary key (int)
- **Name**: Name of the sponsorship level (varchar)
- **Description**: Description of the sponsorship level (text)

### 7. PERFORMANCE
- **Event_id**: Foreign key referencing the event associated with the performance (int)
- **Performance_id**: Primary key (int)
- **Performer_id**: Foreign key referencing the performer involved in the performance (int)
- **Start_time**: Start time of the performance (timestamp)
- **End_time**: End time of the performance (timestamp)
- **Cost**: Amount taken by the performer to perform in an event (decimal)

### 8. PERFORMER
- **Performer_id**: Primary key (int)
- **User_id**: Foreign key referencing the user associated with the performer (int)
- **Stage_name**: Performer’s stage name (varchar)
- **Genre**: Genre of the performer (varchar)
- **Bio**: Performer’s biography (text)

### 9. ROLE
- **Role_id**: Primary key (int)
- **Name**: Name of the role (varchar)
- **Description**: Description of the role (text)

### 10. REGISTRATION
- **Registration_id**: Primary key (int)
- **Participant_id**: Foreign key referencing the participant registered for an event (int)
- **Event_id**: Foreign key referencing the event for which registration is done (int)
- **Payment_method**: Method of payment (varchar)
- **Payment_status**: Status of payment (varchar)
- **Registration_date**: Date of the registration (date)

### 11. LOCATION
- **Location_id**: Primary key (int)
- **Name**: Name of the location (varchar)
- **Address**: Address of the location (text)
- **City**: City where the location is situated (varchar)
- **State**: State where the location is situated (varchar)
- **Country**: Country where the location is situated (varchar)

### 12. EVENT
- **Event_id**: Primary key (int)
- **Fest_id**: Foreign key referencing the fest associated with the event (int)
- **Name**: Name of the event (varchar)
- **Start_date**: Date when the event begins (date)
- **End_date**: Date when the event ends (date)
- **Venue_id**: Foreign key referencing the venue of the event (int)
- **Description**: Description of the event (text)
- **Participation**: Number of current participants in an event (int)
- **Ticket_price**: Price of the ticket (decimal)
- **Organizer_id**: Foreign key referencing the organizer organizing the event (int)
- **Skill_level**: Skill required to participate in the event (text)

## Functions
1. `total_profit_from_fest(fest_id int)`: Returns the total profit from the specified fest.
2. `total_amount_from_ticket(fest_id int)`: Returns the total amount obtained from selling tickets for the specified fest.
3. `locations_performance(performer_id int)`: Returns the locations where the specified performer has performed.
4. `total_amount_from_sponsors(fest_id int)`: Returns the total amount obtained from sponsors of the specified fest.
5. `total_participant_of_fest(fest_id int)`: Returns the total number of participants in the specified fest.
6. `perct_ticket_sponsors(fest_id int)`: Returns the percentage of the amount obtained from sponsors and tickets for the specified fest.
7. `total_cost_performance(fest_id int)`: Returns the total cost required for all performances in the specified fest.
8. `top_sponsors(fest_id int)`: Returns the top sponsor for the specified fest.
9. `top_event(fest_id int)`: Returns the most popular event of the specified fest.

## Triggers
1. **participant_insert**: Creates views for the participant and registration relations and grants permissions.
2. **sponsorship_insert**: Creates views for the sponsorship relation and grants permissions.
3. **event_insert**: Creates views for the event, registration, and performance relations and grants permissions.
4. **fest_insert**: Creates views for the fest, event, and sponsorship relations and grants permissions.
5. **performer_insert**: Creates views for the performer and performance relations and grants permissions.
6. **user_insert**: Creates the user role with the username as the role name and the password as the role password.
7. **upd_budget**: Updates the budget of the fest after a new sponsor is inserted.

## Roles

### Group Roles
1. **Super_participant**
   - Select on specific columns from location, fest, event, venue, performance, performer, and users.
2. **Super_sponsor**
   - Select on sponsor_level, location, fest, event, venue, performance, performer, and users.
3. **Super_event_organizers**
   - Select and update on venue.
   - Select on fest, location, performer, and users.
4. **Super_fest_organizers**
   - Select on location.
   - Select, update, and insert on venue and sponsor_level.
   - Select on participant, performance, registration.
   - Select and insert on performer.
5. **Super_performer**
   - Select on location, fest, event, venue, performance, and users.

### User Roles
- **Participant**
  - Select on participant and registration views.
  - Grant super_participant.
- **Sponsor**
  - Select and update on sponsorship view.
  - Grant super_sponsor.
- **Event_Organizer**
  - Select and update on event view.
  - Select on eventregistration view.
  - Select, insert, update, and delete on eventperformance view.
  - Grant super_event_organizer.
- **Fest_Organizer**
  - Select and update on fest view.
  - Select, update, and insert on festevent view.
  - Select, delete, update, and insert on festsponsors view.
  - Grant super_fest_organizer.
- **Performer**
  - Select and update on performer view.
  - Select on performance view.
  - Grant super_performer.

## Views
- **Participant Views**
  - `participant_<username>`: View for participant's own participation.
  - `registration_<username>`: View for participant's own event registrations.
- **Sponsor Views**
  - `sponsorship_<username>`: View for sponsor's own sponsorships.
- **Event Organizer Views**
  - `event_<username>`: View for organizer's own events.
  - `eventregistration_<username>`: View for organizer's event registrations.
  - `eventperformance_<username>`: View for organizer's event performances.
- **Fest Organizer Views**
  - `fest_<username>`: View for organizer's own fests.
  - `festevent_<username>`: View for organizer's events under their fests.
  - `festsponsors_<username>`: View for organizer's sponsors of their fests.
- **Performer Views**
  - `performer_<username>`: View for performer's own information.
  - `performance_<username>`: View for performer's own performances.

## Indices
1. `CREATE INDEX idx_users_user_id_hash ON users USING hash (user_id);`
2. `CREATE INDEX idx_role_role_id_hash ON role USING hash (role_id);`
3. `CREATE INDEX idx_event_fest_id_event_id ON event USING hash (fest_id, event_id);`
4. `CREATE INDEX idx_registration_event_id ON registration USING hash (event_id);`
5. `CREATE INDEX idx_sponsorship_fest_id ON sponsorship USING hash (fest_id);`
6. `CREATE INDEX idx_participant_fest_id ON participant USING hash (fest_id);`
7. `CREATE INDEX idx_fest_fest_id ON fest USING hash (fest_id);`
8. `CREATE INDEX idx_performance_event_id ON performance USING BTREE (event_id);`

## Conclusion
The Fest Management System is designed to efficiently manage and organize various aspects of festivals, providing necessary functionalities and ensuring data integrity and security through the use of triggers, roles, views, and indices. This system facilitates effective management and access control for different types of users involved in the fest activities.
