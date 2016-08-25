# za_entities
Aleph Extractors for South African entity formats

## Development

### Setup

```
# make a virtualenv at, say, env

pip install -r requirements.txt
source env/bin/activate

# Install aleph deps for testing
pip install -r env/src/aleph/requirements.txt
```

- To run your dev repo in aleph, you can install this repo in editable form in your local aleph python environment with `python setup.py develop`. Make sure the aleph environment is active.
- If you're running your local aleph using docker (recommended, because of all the deps), you can map this repo into the docker container, change to this directory, and then install it.
- Remember to restart the worker each time you want to try out you changes

### Testing

    nosetests