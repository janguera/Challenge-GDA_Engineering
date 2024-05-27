# Challenge-GDA_Engineering
Engineering challenge to design and develop a web API that identifies if comments on a given subfeddit or category are positive or negative.

# Introduction
The `docker-compose.yml` file provides access to `Feddit` which is a fake reddit API built to complete the Allianz challenge. 

# How-to-run
1. Please make sure you have docker installed.
2. To run `Feddit` API locally in the terminal, replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> up -d`. It should be available in [http://0.0.0.0:8080](http://0.0.0.0:8080). 
3. To stop `Feddit` API in the terminal,  replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> down`.

# Feddit API Specification
Please visit either [http://0.0.0.0:8080/docs](http://0.0.0.0:8080/docs) or [http://0.0.0.0:8080/redoc](http://0.0.0.0:8080/redoc) for the documentation of available endpoints and examples of the responses.
There are 3 subfeddits available. For each subfeddit there are more than 20,000 comments, that is why we use pagination in the JSON response with the following parameters:

+ `skip` which is the number of comments to be skipped for each query
+ `limit` which is the max returned number of comments in a JSON response.

# Feddit API Data Schemas
## Comment

+ **id**: unique identifier of the comment.
+ **username**: user who made/wrote the comment.
+ **text**: content of the comment in free text format.
+ **created_at**: timestamp in unix epoch time indicating when the comment was made/wrote.

## Subfeddit
+ **id**: unique identifier of the subfeddit
+ **username**: user who started the subfeddit.
+ **title**: topic of the subfeddit.
+ **description**: short description of the subfeddit.
+ **comments**: comments under the subfeddit.

# Comment Analysis API Execution

In order to run the comment analysis API locally, you can execute the `docker-compose.yml` file as specified at the beginning of the file. It should be available in [http://127.0.0.1:8000/subfeddit-api/](http://127.0.0.1:8000/subfeddit-api/)

An additional image has been added with the solution, so the database, the Feddit API and the comment analysis API will run under the same host.

# Comment Analysis API Specification
Please visit [http://127.0.0.1:8000/subfeddit-api/docs](http://127.0.0.1:8000/subfeddit-api/docs) for the documentation of available endpoints and examples of the responses.

There are 5 variables to be set in the API, being only the `subfeddit` id mandatory:

+ **subfeddit**:  unique identifier of the subfeddit
+ **comments_limit**: (OPT) maximum number of comments to be analysed
+ **time_range**: (OPT) minutes from the current time to consider the comments.
+ **sorted_results**: (OPT) boolean indicating whether the results should be sorted by the polarity score
