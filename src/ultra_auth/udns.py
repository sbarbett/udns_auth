import requests
from typing import Union

class UltraApi:
    def __init__(self, bu: str, pr: str = None, use_token: bool = False):
        """
        Initialize the UltraApi client.

        Parameters:
        - bu (str): Either username or bearer token based on `use_token` flag.
        - pr (str, optional): Either password or refresh token based on `use_token` flag. Defaults to None.
        - use_token (bool, optional): If True, treats `bu` as bearer token and `pr` as refresh token. Defaults to False.

        Raises:
        - ValueError: If `pr` is not provided when `use_token` is True.
        """
        self.base_url = "https://api.ultradns.com"
        self.access_token = str()
        self.refresh_token = str()

        if use_token:
            self.access_token = bu
            self.refresh_token = pr
            if not self.refresh_token:
                print(
                    "Warning: Passing a Bearer token with no refresh token means the client state will expire after an hour.")
        else:
            self.username = bu
            self.password = pr
            if not self.password:
                raise ValueError("Password is required when providing a username.")
            self._auth()

    def _auth(self):
        """Authenticate using username and password.

        Returns:
        - dict: The response body.

        Raises:
        - Exception: If the status is an error.
        """
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        resp = requests.post(f"{self.base_url}/authorization/token", data=payload)
        resp.raise_for_status()
        self.access_token = resp.json().get('accessToken')
        self.refresh_token = resp.json().get('refreshToken')

    def _refresh(self):
        """Refresh the access token using the refresh token.

        Raises:
        - Exception: If the refresh token is not set.

        Returns:
        - dict: The response body.
        """
        if self.refresh_token:
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
            resp = requests.post(f"{self.base_url}/authorization/token", data=payload)
            resp.raise_for_status()
            self.access_token = resp.json().get('accessToken')
            self.refresh_token = resp.json().get('refreshToken')
        else:
            raise Exception("Error: Your token cannot be refreshed.")

    def _headers(self, content_type: str = None) -> dict:
        """Generate request headers.

        Parameters:
        - content_type (str, optional): The content type of the request. Defaults to None.

        Returns:
        - dict: The request headers.
        """
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "Shane's UDNS Client"
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def post(self, uri: str, payload: str = None, plain_text: bool = False) -> Union[dict, str, bytes]:
        """Make a POST request.

        Parameters:
        - uri (str): The URI to call.
        - payload (str, optional): The payload to send. Defaults to None.

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        return self._call(uri, "POST", payload=payload, plain_text=plain_text)

    def put(self, uri: str, payload: str, plain_text: bool = False) -> Union[dict, str, bytes]:
        """Make a PUT request.

        Parameters:
        - uri (str): The URI to call.
        - payload (string): The payload to send.

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        return self._call(uri, "PUT", payload=payload, plain_text=plain_text)

    def patch(self, uri: str, payload: str, plain_text: bool = False) -> Union[dict, str, bytes]:
        """Make a PATCH request.

        Parameters:
        - uri (str): The URI to call.
        - payload (string): The payload to send.

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        return self._call(uri, "PATCH", payload=payload, plain_text=plain_text)

    def get(self, uri: str, params: dict = {}, content_type: str = None) -> Union[dict, str, bytes]:
        """Make a GET request.

        Parameters:
        - uri (str): The URI to call.
        - params (dict, optional): Query parameters. Defaults to {}.
        - content_type (str, optional): The content type of the request. Defaults to None.

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        # GET requests should always be x-www-form-urlencoded, but the UDNS endpoints inexplicably require "application/json"
        if content_type:
            return self._call(uri, "GET", params=params, content_type=content_type)
        else:
            return self._call(uri, "GET", params=params)

    def delete(self, uri: str, content_type: str = None) -> Union[dict, str, bytes]:
        """Make a DELETE request.

        Parameters:
        - uri (str): The URI to call.
        - content_type (str, optional): The content type of the request. Defaults to None.

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        # DELETE requests should, also, always be x-www-form-urlencoded (but of course they're not)
        if content_type:
            return self._call(uri, "DELETE", content_type=content_type)
        else:
            return self._call(uri, "DELETE")

    def _call(self, uri: str, method: str, params: dict = None, payload: dict = None, retry: bool = True, content_type: str = "application/json", plain_text: bool = False) -> Union[dict, str, bytes]:
        """Make an API call.

        Parameters:
        - uri (str): The URI to call.
        - method (str): The HTTP method to use.
        - params (dict, optional): Query parameters. Defaults to None.
        - payload (dict, optional): The payload to send. Defaults to None.
        - retry (bool, optional): Whether to retry the request if the access token has expired. Defaults to True.
        - content_type (str, optional): The content type of the request. Defaults to "application/json".

        Returns:
        - Union[dict, str, bytes]: The response body.
        """
        # Debugging
        print(type(payload))
        print(payload)
        if plain_text:
            resp = requests.request(method, self.base_url+uri, params=params, data=payload, headers=self._headers(content_type))
        else:
            resp = requests.request(method, self.base_url+uri, params=params, json=payload, headers=self._headers(content_type))

        if resp.status_code == requests.codes.NO_CONTENT:
            # DELETE requests and a few other things return no response body
            return {}

        if resp.headers['Content-Type'] == 'application/zip':
            # Return the bytes. Zone exports return zip files
            return resp.content

        if resp.headers['Content-Type'] == 'text/plain':
            # Return plain text. If you request a zone export with 1 domain, it returns a plain text zone file
            return resp.text

        if resp.status_code == requests.codes.ACCEPTED:
            # If there's a task ID in the header, add it to the JSON so the result can be retrieved
            response_data = resp.json()
            response_data.update({"task_id": resp.headers['X-Task-Id']})
            return response_data

        if resp.status_code == 401 and retry:
            # Refresh the token if it expired, then try again
            self._refresh()
            return self._call(uri, method, params, payload, False)

        # Raise any error statuses. Since the UDNS API also produces a response body in most cases, print that too
        try:
            resp.raise_for_status()
        except Exception as e:
            print(resp.text)
            raise

        # Everything else should be JSON (hopefully)
        return resp.json()
