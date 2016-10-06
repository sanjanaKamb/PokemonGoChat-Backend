# PokemonGoChat-Backend
Backend of a chat Android application that allows Pokemon Go users to discuss strategies in chat rooms at Gyms. 
This involves the running the backend in Python using Flask on an Amazon EC2 instance. 
Usernames and passwords are stored in Amazon RDS allowing for user authentication securely over HTTPS using RESTful services. 
Elastic Load Balancer has been setup for future scalability. 

ingress_parser.py - Python scripts that logs into Ingress gmail account and talks to the Ingress backend to retrieve gyms/portals for a specified longitude and latitude

server.py - Backend server in Flask that communicates with frontend with rest api and calls ingress_parser for gym/portal locations when requested by frontend Android application.
