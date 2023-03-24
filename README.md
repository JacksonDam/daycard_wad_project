# daycard_wad_project

Deployment instructions:

Clone the repo and change directory
to the cloned folder

Run pip freeze > requirements.txt

Run python manage.py makemigrations daycard
Run python manage.py migrate
Run python manage.py runserver and 
follow the sign up process.

Keep a note of the username used at sign up.

Close the server, then run python populate_daycard.py [YOUR_USERNAME]

This is so that the populate script can friend you with a series of demo users,
so you have posts to view.

NOTE: posts disappear after 24 hours due to the design
of the product. If you are a marker who takes longer
than 24 hours to mark the work, please delete the database,
run python manage.py migrate once again, then sign up and
run the population script again, passing your username as an argument.