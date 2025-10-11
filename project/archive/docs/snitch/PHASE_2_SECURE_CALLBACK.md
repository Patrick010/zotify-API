<!-- ID: DOC-040 -->
# Phase 2: Secure Callback Handling

This document outlines the implementation of secure OAuth callback handling in the Snitch module.

## Overview

The primary goal of Phase 2 is to prevent Cross-Site Request Forgery (CSRF) attacks during the OAuth 2.0 authorization flow. This is achieved by using a `state` token.

The Zotify API, when initiating the authentication request to Spotify, generates a unique, unguessable `state` token. This token is passed to the Snitch listener via a command-line flag. Snitch will then only accept callback requests that include this exact `state` token.

## Logic Flow

1.  **Initiation**: The Zotify API starts the Snitch listener process, passing a unique `state` token as a command-line argument:
    ```bash
    ./snitch -state="some-unguessable-random-string"
    ```

2.  **Listening**: Snitch starts its local HTTP server and waits for a callback on `http://localhost:21371/callback`.

3.  **Validation**: When a request is received, Snitch performs the following checks:
    -   It verifies that a `state` query parameter exists.
    -   It compares the value of the `state` parameter with the `expectedState` token it received on startup.
    -   If the states do not match, the request is rejected with an HTTP 400 Bad Request error, and an error is logged. The server remains running to await a valid request.
    -   If the states match, it proceeds to the next step.

4.  **Code Extraction**: Once the state is validated, Snitch extracts the `code` query parameter.

5.  **Output and Shutdown**:
    -   The extracted `code` is printed to standard output (`stdout`).
    -   A success message is returned to the browser/client.
    -   A graceful shutdown of the HTTP listener is initiated.

This ensures that only legitimate requests originating from the user's own authentication flow (initiated by the Zotify API) are processed.
