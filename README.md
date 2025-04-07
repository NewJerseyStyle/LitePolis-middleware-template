# :rocket: Build Your Own LitePolis Middleware! :rocket:

Welcome, Developer! Ready to extend LitePolis with your own custom functionality? This template is your launchpad for creating powerful middleware modules.

> :heavy_exclamation_mark: LitePolis is FastAPI based, so as middleware the FastAPI middleware.

## Step 1: :clipboard: Grab the Template

Assume your new project is called "litepolis_middleware_auth"

```bash
litepolis-cli create middleware LitePolis-middleware-auth
cd LitePolis-middleware-auth

# or you can also do:
# git clone https://github.com/NewJerseyStyle/LitePolis-middleware-template
# mv LitePolis-middleware-template LitePolis-middleware-auth
# cd LitePolis-middleware-auth
```

**What to Change:**

1.  **`pyproject.toml` - The Control Center:**
    * Open `pyproject.toml`. This file tells Python how to build and manage your package.
    * Find the `[project]` section.
    * **Change `name`**: Replace `"litepolis-middleware-template"` with your unique name, keeping the prefix.
        ```diff
        [project]
        - name = "litepolis-middleware-template"
        + name = "litepolis-middleware-auth" # <-- CHANGE THIS!
        version = "0.0.1" # You might want to reset this to 0.0.1 or 0.1.0
        authors = [
        -    { name = "Your name" }, # <-- CHANGE THIS!
        +    { name = "Your Awesome Name", email = "your.email@example.com" },
        ]
        - description = "The middleware module for LitePolis" # <-- CHANGE THIS!
        + description = "Handles authentication and authorization for LitePolis apps."
        dependencies = [
            "litepolis",
        -    "litepolis-database-example", # <-- Remove or change dependencies as needed
        +    "passlib[bcrypt]",         # Example
        ]
        ```
    * Update `authors`, `description`, and `dependencies` to match *your* project.
    * Check the `[project.urls]` section and update the `Homepage` URL if you host your code elsewhere.

2.  **The Main Code Folder:**
    * Rename the folder `litepolis_middleware_template` to match your package name, but using underscores (`_`) instead of hyphens (`-`).
    * Example: `litepolis_middleware_template` becomes `litepolis_middleware_auth`

3.  **Test File Imports:**
    * Open `tests/test_core.py`.
    * Find the import statement at the top. It needs to reflect your new folder name.
    * Example:
        ```diff
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        - from litepolis_middleware_template.core import add_middleware, DEFAULT_CONFIG
        + from litepolis_middleware_auth.core import add_middleware, DEFAULT_CONFIG # <-- CHANGE THIS!

        # ... rest of the test file
        ```

> **:warning: Super Important Naming Convention:**
> * Your package name in `pyproject.toml` **MUST** start with `litepolis-middleware-`.
> * Your main code directory **MUST** start with `litepolis_middleware_`.
> * Failure to follow this will prevent LitePolis from finding and loading your middleware!

## Step 2: :sparkles: Implement Your Middleware Magic!

Now for the fun part – writing the code that *does* something!

1.  **Navigate to Your Core Logic:**
    * Open the file inside your renamed code folder (e.g., `litepolis_middleware_auth/core.py`).

2.  **Find `add_middleware`:**
    * This function is the entry point LitePolis calls. It receives the FastAPI `app` instance and the configuration specific to your middleware.
    * **This is where you'll add your FastAPI middleware.** You might define a middleware class or function *within* this file (or import it from another file in your package) and then add it to the app using `app.add_middleware(...)`.

    ```python
    # Example: Inside litepolis_middleware_auth/core.py
    from fastapi import FastAPI, Request, Depends
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import Response
    from litepolis import get_config
    import time # Just an example

    # Your configuration defaults (more on this later!)
    DEFAULT_CONFIG = {
        "enabled": True,
        "some_api_key": "replace_this_default_key",
    }

    # --- YOUR MIDDLEWARE LOGIC GOES HERE ---
    class MyCustomMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            start_time = time.time()
            # Do something before the request is processed (e.g., check auth header)
            print(f"Middleware: Processing request {request.url.path}")

            response = await call_next(request) # Process the request

            # Do something after the request is processed
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            print(f"Middleware: Finished processing in {process_time:.4f} secs")
            return response

    # --- / YOUR MIDDLEWARE LOGIC ---


    def add_middleware(app: FastAPI):
        """
        Adds the custom middleware to the FastAPI application.
        Update this docstring to explain YOUR middleware!
        """
        # Use the provided config, falling back to defaults if necessary
        is_enabled = DEFAULT_CONFIG["enabled"]
        try:
            is_enabled = get_config("litepolis_middleware_auth", "enabled")
        except:
            pass

        if is_enabled:
            print(f"Adding MyCustomMiddleware (config: {config})") # Good for debugging
            # *** THIS IS WHERE YOU ADD YOUR MIDDLEWARE ***
            app.add_middleware(MyCustomMiddleware)
            # You might pass config values to your middleware's __init__ if needed
            # app.add_middleware(MyOtherMiddleware, api_key=config.get("some_api_key"))
        else:
            print("MyCustomMiddleware is disabled via configuration.")

    ```

3.  **Update Documentation:**
    * **Crucially, update the docstrings and comments** in `core.py` (especially for `add_middleware` and within your middleware logic). LitePolis uses these comments to generate help and documentation! Explain what *your* middleware does.

## Step 3: :gear: Configure Your Middleware

Your middleware might need settings (API keys, feature flags, database URLs, etc.).

1.  **Default Settings (`DEFAULT_CONFIG`):**
    * Locate the `DEFAULT_CONFIG` dictionary near the top of your `core.py` (e.g., `litepolis_middleware_auth/core.py`).
    * **Modify this dictionary to hold the *default* values for your middleware's configuration.** These are the settings LitePolis will register if no specific overrides are provided during deployment.

    ```python
    # Example: Inside litepolis_middleware_auth/core.py
    DEFAULT_CONFIG = {
        "enabled": True, # Should the middleware run?
        "auth_provider_url": "https://default.auth.example.com",
        "cache_ttl_seconds": 300,
        # Add YOUR default settings here
    }
    ```

2.  **External Dependencies:**
    * If your middleware needs other Python packages (like `requests`, `python-jose`, `passlib`, etc.), **add them to the `dependencies` list** under the `[project]` section in your `pyproject.toml` file.

3.  **Accessing Configuration Safely (Important!):**
    * LitePolis provides a way to get the *current* configuration values (defaults potentially overridden at deployment). However, you need a way to run tests *without* relying on a live LitePolis configuration system.
    * **Use this pattern** inside your middleware code (or related functions) whenever you need to fetch a configuration value:

    ```python
    # Inside your middleware code (e.g., core.py or another module)
    import os
    # from litepolis import get_config # Import this in a real LitePolis env

    # Your default config defined earlier in core.py
    # from .core import DEFAULT_CONFIG

    # --- Configuration Fetching Logic ---
    auth_url = None
    is_enabled = None

    # Check if running under Pytest
    if ("PYTEST_CURRENT_TEST" not in os.environ and
        "PYTEST_VERSION" not in os.environ):
        # NOT running under Pytest: Fetch from live LitePolis config source
        print("Fetching configuration from live source...") # Optional debug msg
        # Replace 'litepolis-middleware-auth' with YOUR package name from pyproject.toml
        # Replace 'auth_provider_url' with YOUR config key
        auth_url = get_config("litepolis-middleware-auth", "auth_provider_url")
        is_enabled = get_config("litepolis-middleware-auth", "enabled")
    else:
        # Running under Pytest: Use default values from DEFAULT_CONFIG
        print("Running under Pytest. Using default configuration.") # Optional debug msg
        auth_url = DEFAULT_CONFIG.get("auth_provider_url") # Use .get() for safety
        is_enabled = DEFAULT_CONFIG.get("enabled", True) # Can provide default here too

    # Now use the determined config values
    print(f"Using Auth URL: {auth_url}")
    print(f"Middleware Enabled: {is_enabled}")
    # --- / Configuration Fetching Logic ---
    ```

## Step 4: :test_tube: Test Your Creation!

Good middleware needs good tests!

1.  **Find the Test File:**
    * Open `tests/test_core.py`.

2.  **Understand the Setup:**
    * It uses `pytest` and FastAPI's `TestClient`.
    * It typically creates a small FastAPI app instance *for testing*, applies your middleware using `add_middleware`, and then makes fake requests to it using `TestClient`.

3.  **Write Your Tests:**
    * **Adapt the existing tests** to match *your* middleware's behavior.
    * Add **new tests** to cover different scenarios:
        * Does it work when enabled?
        * Does it do nothing when disabled (via `DEFAULT_CONFIG` or mocked config)?
        * Does it handle edge cases correctly?
        * If it modifies requests or responses, assert those changes.
    * Ensure your tests correctly use or mock the `DEFAULT_CONFIG` values.

    ```python
    # Example snippet from tests/test_core.py (adapt it!)
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    # Make sure this uses YOUR renamed package!
    from litepolis_middleware_auth.core import add_middleware, DEFAULT_CONFIG

    def create_test_app(**config_overrides):
        app = FastAPI()
        # Apply potential overrides to default config for testing
        test_config = {**DEFAULT_CONFIG, **config_overrides}
        add_middleware(app, **test_config)

        @app.get("/test_route")
        async def read_main():
            return {"msg": "Hello World"}
        return app

    def test_middleware_adds_header_when_enabled():
        # Test with default config (assuming it's enabled by default)
        app = create_test_app()
        client = TestClient(app)
        response = client.get("/test_route")
        assert response.status_code == 200
        # Example: Assert your middleware did something
        assert "X-Process-Time" in response.headers

    def test_middleware_does_not_run_when_disabled():
        # Test explicitly disabling the middleware
        app = create_test_app(enabled=False)
        client = TestClient(app)
        response = client.get("/test_route")
        assert response.status_code == 200
        # Example: Assert your middleware DID NOT do something
        assert "X-Process-Time" not in response.headers

    # --- ADD MORE TESTS FOR YOUR SPECIFIC LOGIC ---
    ```

4.  **Run Your Tests:**
    * From your project's root directory, run `pytest`. Make sure they pass!

## :checkered_flag: You're (Almost) Done!

You've now:

1.  Cloned the template.
2.  Renamed everything to make it uniquely yours.
3.  Implemented your core middleware logic in `core.py`.
4.  Set up default configuration in `DEFAULT_CONFIG`.
5.  Added necessary dependencies in `pyproject.toml`.
6.  Written tests to ensure it works!

**What's Next?**

When you deploy this middleware within the LitePolis ecosystem, LitePolis will:

* Recognize your package because of the `litepolis-middleware-` prefix.
* Read the configuration (`DEFAULT_CONFIG` and any deployment overrides).
* Call your `add_middleware` function to integrate it into the target FastAPI application.
* Use your docstrings for help and documentation.

**Happy Building!** We can't wait to see what amazing middleware you create for LitePolis!