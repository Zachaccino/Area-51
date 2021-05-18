# Build

You can build a docker container image with tag `harvester` using the command below, make sure you are in the folder that contains the `Dockerfile`.

```bash
docker build . -t harvester
```

# Configure

You need to create an environment file, for example, a `.env` file, and making sure the secrets are properly filled. An example of this file `.env.example` is located under this folder. Anyway, the content of the environment file is shown below.

```bash
DB_USERNAME=***
DB_PASSWORD=***
DB_ADDRESS=http://***.***.***.***:***

CONSUMER_KEY=***
CONSUMER_SECRET_KEY=***
ACCESS_TOKEN=***
ACCESS_TOKEN_SECRET=***

HARVESTER_TYPE=[TWEET|TIMELINE]
BBOX_INDEX=[0-3]
```

Note that the environment variable `HARVESTER_TYPE` can be a string of either `TWEET` or `TIMELINE`. When you set it to `TWEET`, you also need to make sure your `BBOX_INDEX` environment variable is also set to an integer between 0 and 3.


# Run

You can run a harvester by using the command below.

```bash
docker run --env-file .env harvester
```


