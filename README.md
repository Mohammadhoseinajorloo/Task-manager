# Discription

in This project, we are trying to impliment a website step by step:

1. create a registration page that stores user information in a database.\
   ## tools:
    - database : mysql database
    - http.serve built in library python
2. create a authentication system in fastapi framework
    ## tools:
    1. fastapi framework 

# TODO LIST

- [x] write routing system
- [x] error handling -> automatically in fastapi
    - [x] datastracture and route serviece 
- [x] fixed not load css file in web server
- [x] redirected registering page in login page and display massage for successful registration. -> automatically in 
fastapi
- [x] README
- [ ] massage system for warning and error in registration user.
- [ ] test all function in project
    - [x] test do get function
    - [x] test processing front data function
- [ ] clean code
    - [ ] separate services in project in folder extention
        - [x] hashing password
        - [x] handling headers (don't) -> **recommend please** -> handel in fastapi
        - [x] routing services **advanture** ==flask like==
        - [x] database services
    - [x] utils in extentions
- [x] update database
- [x] create home page website
- [x] create login page website
- [ ] add redis for caching
