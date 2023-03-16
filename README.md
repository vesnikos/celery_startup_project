# A testing approach for celery/postgresql using pytest 

Testing is needed to demostrate to you or the PO that the code is in a working state. Whenever new changes are made the test verify that previous functionality is still working and that new functionality is working as expected.

This project demostrates a testing approach for celery/postgresql project using pytest as testing framework but also to control the database state. 

#### The tech stack 

 - celery  
 - pytest
 - pytest-celery
 - pytest-postgresql

#### project layout

- `src` - the source code
- `tests` - the tests
- `conftest.py` - pytest configuration file
- `pyproject.toml` - project configuration file (includes dependencies and tasks)


> **Note:** The project is using [poetry](https://python-poetry.org/) to manage dependencies and tasks.

### Installation

```bash
$> poetry install --no-root
```
### Running the tests

```bash
$> poetry run poe test 
```