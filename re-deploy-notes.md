after merging updates to master:
1) `$ heroku run python ./manage.py makemigrations -a lambda-mud-kj`
2) `$ heroku run python ./manage.py migrate -a lambda-mud-kj`
3) `$ heroku run python ./manage.py shell -a lambda-mud-kj`
4) paste `my_create_world.py`