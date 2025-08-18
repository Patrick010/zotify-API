# Snitch Architecture

**Status:** Active
**Date:** 2025-08-18

## 1. Core Design & Workflow (Zero Trust Model)

Snitch is a minimal, self-contained Go application that acts as a temporary, local callback listener for OAuth 2.0 flows. Its architecture is designed around a Zero Trust security model, where the sensitive authorization `code` is protected with end-to-end encryption.

The standard workflow is as follows:
1.  **Initiation (Zotify API):** A user action triggers the need for authentication. The Zotify API generates a short-lived, signed **JSON Web Token (JWT)** to use as the `state` parameter. This JWT contains a unique, single-use `nonce`.
2.  **Launch (Client):** The client application receives the authorization URL (containing the `state` JWT) from the API. It also receives the API's **public key**. The client then launches the local Snitch process, providing it with the public key.
3.  **Callback (Snitch):** The user authenticates with the OAuth provider, who redirects the browser to Snitch's `localhost` listener. The redirect includes the plain-text `code` and the `state` JWT.
4.  **Encryption (Snitch):** Snitch receives the `code`. Using the API's public key, it **encrypts the `code`** with a strong asymmetric algorithm (e.g., RSA-OAEP).
5.  **Handoff (Snitch to API):** Snitch makes a `GET` request over the network to the remote Zotify API, sending the `state` JWT and the `code` as query parameters. (Note: The encryption of the `code` described in this design is a planned future enhancement and is not yet implemented).
6.  **Validation (Zotify API):** The API validates the `state` JWT's signature, checks that the `nonce` has not been used before, and then uses its **private key** to decrypt the `code`.

## 2. Security Model

### 2.1. Browser-to-Snitch Channel (Local)
This channel is secured by **containment**. The Snitch server binds only to the `127.0.0.1` interface, meaning traffic never leaves the local machine and cannot be sniffed from the network. While the traffic is HTTP, the sensitive `code` is immediately encrypted by Snitch before being transmitted anywhere else, providing protection even from malicious software on the local machine that might inspect network traffic.

### 2.2. Snitch-to-API Channel (Remote)
This channel is secured by **end-to-end payload encryption**.
-   **Vulnerability Mitigated:** An attacker sniffing network traffic between the client and the server cannot read the sensitive authorization `code`, as it is asymmetrically encrypted. Only the Zotify API, with its secret private key, can decrypt it.
-   **Defense-in-Depth:** This payload encryption is independent of transport encryption. For maximum security, the API endpoint should still use HTTPS, providing two separate layers of protection.

### 2.3. Replay Attack Prevention
-   **Vulnerability Mitigated:** Replay attacks are prevented by the use of a **nonce** inside the signed `state` JWT. The Zotify API server will reject any request containing a nonce that has already been used, rendering captured requests useless.

### 2.4. Key Management
-   The security of the system depends on the Zotify API's **private key** remaining secret. This key must be stored securely on the server using standard secret management practices.
-   The key pair is designed to be **configurable**, allowing for integration with certificate authorities or custom key pairs.

For a more detailed breakdown of this design, please refer to the canonical design document: **[`PHASE_2_ZERO_TRUST_DESIGN.md`](./PHASE_2_ZERO_TRUST_DESIGN.md)**.
