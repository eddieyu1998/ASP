# ASP
>Fill in the form in the google sheet to indicate who is working on what and avoid concurrency

`$ pip install Pillow` `$ pip install reportlab` in the virtual env 

/login -> admin login lead to invitation management page


/ASP/registration/invitation_id -> use the token generated in the console to register


use the new account to login to their corresponding page

TO-DO: (arranged by importance)
- [ ] Construction 2 things
- [ ] modify the getRoute function to cater for tiebreak
- [x] Form validation (e.g. email format, deplicate username...)
- [x] Clinic->Location migration
- [x] Use HttpResponseRedirect instead for all functions that deals with http POST
- [x] Add image field in Supply and link image files in html
- [x] Modify project structure (make it more modular, divide fuctionalities into apps)
