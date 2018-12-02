# ASP

Pillow and reportlab are required for the implementation, please run the following commands.

`$ pip install Pillow` `$ pip install reportlab`

**Usage:**

/login -> login as admin leads to an invitation management page (create admin account first by: `$ manage.py createsuperuser`)

After logging in as admin, add new invitations as you wish, then send token. A email containing the token is redirected to the console.

/ASP/registration/invitation_id -> use the link generated in the console to register as new user

In the registration page, follow the instruction as stated to register. If the new user is a clinic manager, he should input the full name of the clinic he is working in. Registration would not be accepted if the clinic is not in the database.

After successful login, the user will be redirected to the page corresponding to his role.

**Notes:**

All assumptions and constraints are as stated in the project description.

All emails are redirected to the console.

For deciding itineraries of equal distance, we will select the itinerary that delivers the highest priority orders earliest in the route. Only the priority of the orders in the same step of the routes would be considered at each comparasion.  
The following examples illustrate that:

route 1: A(High) -> B(Medium) -> C(Low)  
route 2: C(Low) -> B(Medium) -> A(High)  
route 1 is selected

route 1: A(High) -> B(Medium) -> C(High, Low)  
route 2: C(High, Low) -> B(Medium) -> A(High)  
route 2 is selected

route 1: A(High) -> B(High) -> C(Medium)  
route 2: A(High) -> C(Medium) -> B(High)  
route 1 is selected

route 1: A(High) -> B(Low) -> C(High, High, Low)  
route 2: B(Low) -> C(High, High, Low) -> A(High)  
route 1 is selected
