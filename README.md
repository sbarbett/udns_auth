# ultra_auth

A compact Python client for managing a connection with the UltraDNS API. For the "official," and much more ambitious client, go [here](https://github.com/ultradns/python_rest_api_client).

## Features

- Support for authenticating with username and password, or directly with a bearer token.
- Automatic token refreshing when the token expires.
- Built-in handling of various content types.

## Installation

You can easily install `ultra_auth` using `pip`:

```bash
pip install ultra_auth
```

Once installed, you can use the ultra_auth module in your Python scripts:

```python
from ultra_auth import UltraApi
client = UltraApi(args)
```

## Usage

### Authenticating using Username and Password

```python
client = UltraApi(your_username, your_password)
```

### Authenticating using Bearer Token

```python
client = UltraApi(your_bearer_token, use_token=True)
```

### Authenticating using Bearer Token and Refresh Token

```python  
client = UltraApi(your_bearer_token, your_refresh_token, True)
``` 

### Making API Calls

```python
# Make a GET request
response = client.get("/ultra/api/endpoint")

# Make a POST request
response = client.post("/ultra/api/endpoint", payload={"key": "value"})

# ... similarly for PUT, PATCH, DELETE
```

## Response Handling

The client can return data in the form of dictionaries, strings, or bytes depending on the response content type.

For example:
1. The zone export endpoint, when requesting more than one zone, will return a zip file
2. The zone export endpoint, when requesting one zone, returns a plain text response
3. Most endpoints return JSON

## Note

Using a bearer token without a refresh token means the client state will expire in approximately 1 hour (assuming the token was just generated). Be warned.

## Contribute

Contributions are always welcome! Please open a pull request with your changes, or open an issue if you encounter any problems or have suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
