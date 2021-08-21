# discourse
A place for discussions.

<br>
<div align="center"> Service that allows users to discuss topics in academic way and write articles of various themes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Discourse Features

- [x] To be updated...



### Run Discourse locally

From project root directory run `docker-compose build`. Then run `docker-compose up`. In case you do not have `docker` and `docker-compose`, install them on your machine and try again.

### Migrations
Go inside the container: `docker exec -it dicsourse bash`. Now that you are inside the container run the commands: `./manage.py makemigrations` and `./manage.py migrate`

## Testing
to-do: add commands
