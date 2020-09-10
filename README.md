# udacity-fsnd-capstone

This is the capstone project for my Full Stack Web Development Nanodegree. Dependencies can be viewed in `requirements.txt`

https://hcndcasting.herokuapp.com/

## API

GET '/' Returns "Hello World"
GET '/movies' Returns a list of the movies in json format
GET '/actors' Returns a list of the actors in json format
POST '/movies' Adds a movie to the database
POST '/actors' Add an actor to the database
PATCH '/actors/int:actor_id' Updates an existing actor in the database
PATCH '/movies/int:movie_id' Updates an existing movie in the database
DELETE '/movies/int:movie_id' Deletes a movie from the database
DELETE '/actors/int:actor_id' Deletes an actor from the database

## Roles and Permissions

### Executive Producer

- Can get actors
- Can get movies
- Can add actors
- Can add movies
- Can update actors
- Can update movies
- Can delete actors
- Can delete movies

### Casting Director

- Can get actors
- Can get movies
- Can add actors
- Can update actors
- Can update movies
- Can delete actors

### Casting assistant

- Can get actors
- Can get movies
