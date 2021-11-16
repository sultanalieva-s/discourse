# discourse
A place for discussions.

<br>
<div align="center"> Service that allows users to discuss topics in academic way and write articles of various themes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Discourse Features

- [x]   CRUD operations
- [x]   Filter, Search
- [x]   Ability to add articles to favorites
- [x]   Registration, Login
- [x]   Password Reset
- [x]   Comments
- [x]   Ability to rate articles
- [x]   Recommendation system which is based on previously liked articles by a user
- [x]   Automated Deployment(planned)
- [x]   Unit Tests Coverage(planned)

### Run Discourse locally

From project root directory run `docker-compose build`. Then run `docker-compose up`. In case you do not have `docker` and `docker-compose`, install them on your machine and try again.

### Migrations
Go inside the container: `docker exec -it dicsourse bash`. Now that you are inside the container run the commands: `./manage.py makemigrations` and `./manage.py migrate`

## Testing
Go inside the container: docker exec -it discourse bash. Then, run the command: ./manage.py test
