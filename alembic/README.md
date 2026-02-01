### Create new migrations
```
alembic revision -m ""
```

### Upgrade latest migrations
```
alembic upgrade head
```

### Down migrations 1 step
```
alembic downgrade -1
```
