## How to run

- See Makefile

### run

`$ make run`

## How to deploy slack bot

`$ make deploy`

### Troubleshoot

1. Vercel serverless maximum size is 250MB

`du -h -d 1 .venv/lib/python3.11/site-packages | sort -h` to check package size

### VS code interpreter setting

cmd + p > interpreter

`apps/api/.venv/bin/python`

### Generate Requirements.txt

Generate requirements.txt using Poetry package manager:

```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

Python monorepo info:
https://medium.com/@ashley.e.shultz/python-mono-repo-with-only-built-in-tooling-7c2d52c2fc66
