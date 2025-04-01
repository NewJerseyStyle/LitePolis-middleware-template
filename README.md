# LitePolis-middleware Template

This repository serves as a template for creating middleware modules for LitePolis. It provides a basic structure and example code to guide you through the process.

> :warning: Keep the prefix "litepolis-middleware-" and "litepolis_middleware_" in the name of package and directories to ensure the LitePolis package manager will be able to recognize it during deployment.

## Getting Started

1.  **Clone the Repository:** Start by cloning this repository to your local machine.

2.  **Rename the Package:** Update the package name in the following files:
    * **`setup.py`**: Change `name='litepolis-middleware-template'` to your desired package name (e.g., `litepolis-middleware-auth`). Also, update the `version`, `description`, `author`, and `url` fields accordingly.
    * **`tests/test_core.py`**: Update the import statements to reflect your new package name. For example, change `from litepolis_middleware_template.core import add_middleware` to `from litepolis_middleware_auth.core import add_middleware`.
    * Rename the folder `litepolis_middleware_template` to your new package name (e.g., `litepolis_middleware_auth`).

3.  **Implement Middleware Logic:** Modify the `litepolis_middleware_template/core.py` file (or the renamed equivalent) to implement your middleware logic. This includes defining the middleware functionality. The `DEFAULT_CONFIG` dictionary in `core.py` allows for default configuration settings. Ensure you update the comments in your code to accurately reflect the middleware's functionality, as these will be used for documentation.

4.  **Testing:** The `tests/test_core.py` file contains example tests using Pytest and FastAPI's `TestClient`. Update these tests to cover your middleware's functionality. Ensure your tests correctly use `DEFAULT_CONFIG` where necessary and properly set up the FastAPI test application instance for testing. Ensure the tests run successfully after making changes.

## Key Files and Modifications

* **`setup.py`**: This file contains metadata about your package. **Crucially**, you need to change the `name` field to your package's unique name. Also, update the `version`, `description`, `author`, and `url` fields as needed.

* **`litepolis_middleware_template/core.py`**: This file contains the core logic for your module, including the `add_middleware` function and the `DEFAULT_CONFIG` dictionary. The `DEFAULT_CONFIG` dictionary provides default configuration settings that will be registered with LitePolis. Implement your middleware logic within the `add_middleware` function. **Important:** Update the comments for documentation.

* **`tests/test_core.py`**: This file contains tests for your module. Update the tests to reflect your changes in `core.py`. Thorough testing is essential for ensuring the correctness of your module. Ensure your tests correctly set up the FastAPI test application and utilize `DEFAULT_CONFIG` as needed.

## Important Considerations

* **Documentation:** Well-documented code is crucial for maintainability and collaboration. Ensure your middleware logic in `core.py` has clear and comprehensive comments. These comments will be used to generate documentation for LitePolis.

* **Testing:** Write comprehensive tests to cover all aspects of your middleware module. This will help catch errors early and ensure the stability of your code.

* **Dependencies:** If your module requires external libraries, add them to the `install_requires` list in `setup.py`. Also list FastAPI-specific dependencies in the `litepolis_middleware_template/dependencies.py` file.

* **`DEFAULT_CONFIG` and Middleware Logic:** The `DEFAULT_CONFIG` dictionary defined in `core.py` is crucial. Its contents will be registered with the LitePolis configuration system upon deployment. Ensure it contains appropriate default values for your middleware. FastAPI middleware logic defined in `core.py` is also essential, as LitePolis will use it to integrate your middleware into applications.

## About `dependencies.py`

Contains definitions for FastAPI dependencies (using `fastapi.Depends`) needed by your middleware. Defining them here helps LitePolis manage and potentially override or inject dependencies during deployment.

## About `DEFAULT_CONFIG`

This dictionary, defined in `core.py`, holds default configuration values for your middleware module. These values will be registered with the LitePolis configuration system when the module is deployed. If modified configurations are provided during deployment, they will override these defaults. Settings can be fetched within your code (or other services) using the `get_config(<package-name>, <configuration-key>)` function provided by LitePolis infrastructure, which will return the currently active value.

## Recommended Pattern for Accessing Configuration

To ensure automated tests (Pytest) do not rely on live configuration sources, use the following pattern to fetch configuration values. This pattern checks for environment variables set by Pytest (`PYTEST_CURRENT_TEST` or `PYTEST_VERSION`) to determine the execution context.

```python
import os
# Assuming get_config is available for fetching live config
# from litepolis import get_config

# Define default values suitable for testing environment
DEFAULT_CONFIG = {
    "some_api_key": "test_key_123"
    # Add other necessary default config values here
}

# Configuration Fetching Logic
db_url = None
some_key = None

# Check if running under Pytest
if ("PYTEST_CURRENT_TEST" not in os.environ and
    "PYTEST_VERSION" not in os.environ):
    # NOT running under Pytest: Fetch from live source
    print("Fetching configuration from live source...") # Optional debug msg
    # Replace with actual service name and key
    some_key = get_config("your_middleware_name", "some_api_key")
else:
    # Running under Pytest: Use default values
    print("Running under Pytest. Using default configuration.") # Optional debug msg
    db_url = DEFAULT_CONFIG["database_url"]
    some_key = DEFAULT_CONFIG["some_api_key"]

# Use the determined config values (db_url, some_key)
print(f"Using Database URL: {db_url}")
print(f"Using API Key: {some_key}")

```

**Guidance:**

* Apply this pattern for any configuration that differs between test and live environments.
* Ensure `DEFAULT_CONFIG` is defined with appropriate test values.
* Remember to `import os`.
* Use the actual `get_config` function provided by the LitePolis environment when not running tests.
