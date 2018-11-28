# ASP

`$ pip install Pillow` `$ pip install reportlab` in the virtual env 

**There is some changes in new_data.py, please delete all old data from database and import the new data**
1. delete db.sqlite3, every files in migrations except `__init__.py`
2. makemigrations and migrate
3. `python manage.py shell`, `from ASP.models import *`, then copy and paste all data 

**Usage:**

/login -> login as admin leads to an invitation management page (create admin account first: `$ manage.py createsuperuser` )

add new invitations as you wish, then send token

/ASP/registration/invitation_id -> use the link generated in the console to register

use the new account to login to their corresponding page


**Notes:**

All assumptions and constraints are as stated in the project description

for deciding itineraries of equal distance, we will select the itinerary that delivers the highest priority orders earliest in the route.  
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
