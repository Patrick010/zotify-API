# Design: Snitch Phase 2 - Zero Trust Secure Callback

**Status:** Proposed
**Author:** Jules
**Date:** 2025-08-16
**Supersedes:** `PHASE_2_SECURE_CALLBACK.md`

## 1. Purpose

This document specifies a new, more robust security design for the Snitch OAuth callback flow, built on Zero Trust principles. It replaces the previous "Secure Callback" design with a model that provides end-to-end encryption for the sensitive authorization `code` and protects against replay attacks.

## 2. Core Design: Asymmetric Cryptography with a Nonce

The new design eliminates the previous model's reliance on the security of the local network. It achieves this by encrypting the sensitive payload itself and by making the transaction verifiable and non-repeatable.

### 2.1. The Workflow

1.  **Setup:** The Zotify API maintains a public/private key pair (e.g., RSA 2048). The private key is kept secret on the server. The public key is distributed with the client application that launches Snitch.

2.  **Initiation (Zotify API):**
    *   When a user initiates a login, the Zotify API generates a `state` parameter. This will be a short-lived, signed **JSON Web Token (JWT)**.
    *   The JWT payload will contain a cryptographically secure, single-use **`nonce`** and a `session_id` to track the login attempt.

3.  **Callback (Snitch on Client Machine):**
    *   The user authenticates with the OAuth provider (e.g., Spotify).
    *   The provider redirects the user's browser to Snitch (`http://127.0.0.1:4381/login`) with the plain-text `code` and the `state` JWT.
    *   Snitch receives the `code`.
    *   Using the **API's public key** (which it has locally), Snitch **encrypts the `code`** using a strong asymmetric algorithm (e.g., RSA-OAEP with SHA-256).
    *   Snitch makes a `POST` request to the remote Zotify API, sending the `state` JWT and the newly **encrypted `code`**.

4.  **Validation (Zotify API):**
    *   The API receives the request.
    *   **Replay Attack Prevention:** It first validates the `state` JWT's signature. It then extracts the `nonce` and checks it against a cache of recently used nonces. If the nonce has been used, the request is rejected. If it's new, the API marks it as used.
    *   **Secure Decryption:** The API uses its **private key** to decrypt the encrypted `code`.
    *   The flow then continues with the now-verified, plain-text `code`.

### 2.2. Key Configurability
- The Zotify API's public/private key pair will be configurable.
- The server will load its private key from a secure location (e.g., environment variable, secrets manager, or an encrypted file).
- The client application that launches Snitch will be responsible for providing Snitch with the corresponding public key. This allows for integration with automated certificate management systems like ACME if desired in the future.

### 2.3. Cipher Suites
- The implementation must use strong, modern cryptographic algorithms.
- **Asymmetric Encryption:** RSA-OAEP with SHA-256 is recommended.
- **JWT Signing:** RS256 (RSA Signature with SHA-256) is recommended.
- Weak or deprecated ciphers (e.g., MD5, SHA-1) are forbidden.

## 3. Relationship with Transport Encryption (HTTPS)

This payload encryption mechanism is a separate layer of security from transport encryption (TLS/HTTPS). They are not mutually exclusive; they are complementary.

-   **Payload Encryption (this design):** Protects the `code` from the moment it leaves Snitch until it is decrypted inside the API server. This protects the secret even if the channel is compromised.
-   **Transport Encryption (HTTPS):** Protects the entire communication channel between Snitch and the API.

**Recommendation:** For a production environment, **both** should be used. This provides defense-in-depth: an attacker would need to break both the TLS channel encryption *and* the RSA payload encryption to steal the `code`. This design ensures that even without HTTPS, the `code` itself remains secure, but it does not protect the rest of the request/response from inspection. The documentation will make it clear that HTTPS is still highly recommended for the API endpoint.

## 4. Implementation Impact
- **Zotify API:** Requires significant changes to the auth callback endpoint to handle JWT validation, nonce checking, and RSA decryption. It also requires a key management solution.
- **Snitch:** Requires changes to add the RSA encryption logic using the provided public key.
- **Client Application:** The application that launches Snitch must be able to receive the API's public key and pass it securely to the Snitch process.
