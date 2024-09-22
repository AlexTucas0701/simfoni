# Molyneu - GitHub Repository Search Application

This is a full stack web application which aims to show the github resources (Users, Repositories) by searching them.

## How to run this project?
1. Prepare the environment.
    - Setup the docker.
    - Prepair the redis cluster.
        - Setup the redis server on local or cloud.
        - Get the connection string for the service.
        - In case of the local, you can specify like this `redis://:yourpassword@localhost:6379`
    - [Optional] Prepare the github account and personal token.
        - Go to the token setting pages of the github: [HERE](https://github.com/settings/tokens)
        - Generate the token. No permission is required for github search API.
2. Prepare the .env file
    - With github personal acces token.
        ```bash
        GITHUB_PAT=
        REDIS_CONNECTION_URL=
        ```
    - Without github personal acces token.
        ```bash
        REDIS_CONNECTION_URL=
        ```
3. Run using the docker cli.
    ```bash
    docker compose -f docker-compose-dev.yml up
    ```
4. Open this [page](http://localhost:3000/)


## Project description

1. Library Usage
    - **backend/pydantic**: Pydantic is a Python library that provides data validation and settings management using Python type annotations, ensuring structured data is parsed, validated, and converted efficiently. That is used to parse the **GitHub API response** and **responded data from the frontend**.
    - **frontend/axios**: Axios is a promise-based HTTP client for JavaScript that simplifies making asynchronous requests to external APIs, allowing easy handling of request and response data, as well as errors, within frontend applications.
    - **frontend/reduxjs-toolkit**: Redux Toolkit is a library that simplifies the use of Redux by providing a standardized approach for managing application state, offering pre-configured tools for reducers, actions, and middleware to streamline development.
    - **frontend/redux-persist**: Redux Persist is a library that enables the persistence of Redux store data across sessions by saving it to storage (like localStorage or sessionStorage), ensuring the state is restored when the application reloads. This library is used for **local caching on the frontend**, so **even if the page is refreshed**, the cached data in **local storage** remains available until the user manually clears it.

2. Backend
    - **Cache Name Prefix for API Search Result**: We used a prefix to identify that the cache is being used for the GitHub search API. Since the cache name is generated dynamically based on the search parameters (like search type and keyword), it can sometimes be difficult to identify the caches precisely. By using the prefix, even if we need to use the cache for other purposes, we can easily differentiate and organize the caches based on their functionality.
    - **pydantic_exception_handler**: This decorator is used to catch and handle ValidationError exceptions raised by Pydantic during request parameter validation. If invalid data is passed to the API, the decorator intercepts the exception, extracts the specific validation errors, and returns a structured response with the error messages and an HTTP status code (defaulting to 400). This ensures that users are informed about the exact issues with their input in a clear and standardized format.
    - **max_retry_exceed_exception_handler**: This decorator handles MaxRetryExceedException errors, which occur when the GitHub API rate limits are exceeded. When this exception is caught, the decorator responds with an error message prompting the user to "Try again after a while," and returns an HTTP status code of 429 (Too Many Requests). This prevents further retries and ensures users are aware that they need to wait before making additional requests.
    - **Singleton pattern for GitHubSearchService**
        - **Efficient resource management**: By maintaining a single instance of the GitHubSearchService, the application reuses the same HTTP session (`self.__session`) and cache service (`self.__cache`), avoiding unnecessary object creation. This improves performance by reducing the overhead of establishing multiple HTTP connections and managing multiple caches.
        - **Consistent caching**: Since the search results are cached, using a Singleton ensures that all parts of the application interact with the same cache, preventing inconsistent data from being stored or retrieved. This is particularly important when making repeated requests to the GitHub API, as it minimizes redundant API calls and helps avoid rate limit issues.
        - **Global state management**: The Singleton pattern simplifies managing global state, such as authentication headers (using GitHub PAT) or the cache. Having a single instance guarantees that all searches and API requests share the same configuration and state, reducing potential bugs related to state inconsistencies.

3. Frontend:
    - **Querying search parameters**: Use the query parameters to specify the search criteria in the frontend router. For example, we have `http://localhost:3000/?keyword=tht&type=user`, where the `keyword` parameter represents the search term (e.g., "tht"), and the `type` parameter defines the search category (e.g., "user"). These query parameters are extracted and passed to the backend service to execute the appropriate GitHub search based on the specified criteria.
    - **Persist storage of the cache using the local storage**: We use `redux-persist` to enable persistence of the cache in local storage. This ensures that cached data, such as GitHub search results, remains available across browser sessions, even after a page refresh or closing the browser. The `persistReducer` is applied to the cacheControlReducer, allowing the specific slice of state responsible for caching (`cached`) to be saved and rehydrated from local storage.
