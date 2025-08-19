# Proposal: Plugin-Driven Multi-Source Metadata System

**Date:** 2025-08-18
**Author:** Jules
**Status:** Proposed

---

## 1. Executive Summary

This document proposes the creation of a **Plugin-Driven Multi-Source Metadata System**. This new core component of the Zotify Platform will transform it from a single-source API into a powerful, extensible, and unified engine for searching and managing music metadata from a variety of sources.

The current architecture is limited to the single, hard-coded Spotify provider. This proposal leverages the `DYNAMIC_PLUGIN_PROPOSAL.md` to create a system where any metadata source—be it another streaming service, a local file library, or a torrent index—can be integrated as a self-contained, installable plugin.

By using a flexible document-oriented database for normalized metadata and a dedicated vector store for semantic embeddings, the system will provide a single, source-agnostic API for both structured and natural language queries. This will enable complex, cross-provider queries that are impossible today, such as "find all progressive rock albums from the 1970s that are available on Spotify but are missing from my local FLAC library."

This proposal outlines the system architecture, data model, API integration, security model, and a phased implementation plan. Adopting this architecture is the next logical step in fulfilling the project's core mission of becoming a truly provider-agnostic and extensible framework.

---

## 2. Core Concepts & Principles

- **Everything is a Plugin:** Each distinct source of metadata is treated as a plugin. This includes the existing Spotify integration, which will be refactored into the first official metadata plugin.
- **Dynamic Discovery:** The system will automatically discover and integrate any installed metadata plugins using the `entry_points` mechanism detailed in the `DYNAMIC_PLUGIN_PROPOSAL.md`. No manual configuration is needed to enable a new source.
- **Centralized Ingestion, Decentralized Logic:** A central `MetadataService` orchestrates the ingestion process, but the logic for fetching and parsing data remains encapsulated within each plugin.
- **Unified Querying:** The user interacts with a single set of query endpoints, regardless of how many metadata plugins are active. The system presents a unified, aggregated view of all available information.
- **Separation of Metadata and Media:** The system stores only metadata and pointers (e.g., file paths, URLs, URIs). The media files themselves are not stored or managed by this system.

---

## 3. System Architecture

The proposed system consists of three new major components that integrate with the existing Zotify API architecture.

```
+--------------------------------+
|       Zotify Core API          |
|  (FastAPI, Services, Routes)   |
+--------------------------------+
             |
             v
+--------------------------------+
|    New: MetadataService        |
| (Plugin Discovery, Orchestration)|
+--------------------------------+
             |
             +------------------------------------+
             |                                    |
             v                                    v
+-----------------------------+   +--------------------------------+
|      Storage Layer          |   |      Plugin Host                 |
|                             |   | (Python Environment)           |
| +-------------------------+ |   |                                |
| |   Document Store        | |   | +----------------------------+ |
| |   (e.g., MongoDB)       | |   | | zotify.metadata.providers  | |
| +-------------------------+ |   | +----------------------------+ |
|                             |   |             ^                  |
| +-------------------------+ |   |             | (registers)      |
| |   Vector Store          | |   | +-----------+----------------+ |
| |   (e.g., FAISS)         | |   | | Plugin 1: Spotify        | |
| +-------------------------+ |   | +----------------------------+ |
|                             |   | +----------------------------+ |
| +-------------------------+ |   | | Plugin 2: Local Files    | |
| |   Relational DB         | |   | +----------------------------+ |
| | (Postgres - for users)  | |   | +----------------------------+ |
| +-------------------------+ |   | | Plugin 3: ...            | |
|                             |   | +----------------------------+ |
+-----------------------------+   +--------------------------------+
```

### 3.1. Metadata Ingestion Plugins

This system introduces a new plugin entry point: `zotify.metadata.providers`. Any installed Python package that registers a plugin against this entry point will be discovered at runtime.

Each plugin must implement a `BaseMetadataProvider` interface:

```python
# In a new file, e.g., api/src/zotify_api/metadata/base.py

from abc import ABC, abstractmethod

class BaseMetadataProvider(ABC):
    # Unique name for the plugin, e.g., "spotify", "local_files"
    name: str

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """ Returns the Pydantic schema for this provider's configuration. """
        pass

    @abstractmethod
    def configure(self, config: Dict[str, Any]):
        """ Configures the provider instance with user-specific settings. """
        pass

    @abstractmethod
    async def ingest(self) -> AsyncIterator[Dict[str, Any]]:
        """
        An async generator that fetches raw metadata from the source
        and yields it one item at a time.
        """
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a raw data item and transforms it into the Common Metadata Schema.
        """
        pass

    @abstractmethod
    async def generate_embeddings(self, normalized_data: Dict[str, Any]) -> List[float]:
        """
        Takes normalized data and generates a vector embedding for semantic search.
        """
        pass
```

### 3.2. MetadataService

A new singleton service, `MetadataService`, will be added to the Core API. It will be responsible for:
- **Plugin Management:** Discovering, loading, and managing instances of all installed metadata plugins.
- **Ingestion Orchestration:** Periodically (or on-demand via an API call) triggering the `ingest()` method on each active plugin.
- **Processing Pipeline:** For each item yielded by a plugin's `ingest()` method, the service will:
    1. Call the plugin's `normalize()` method.
    2. Store the normalized document in the Document Store (MongoDB).
    3. Call the plugin's `generate_embeddings()` method.
    4. Store the resulting vector in the Vector Store (FAISS).
- **Query Orchestration:** Receiving queries from the API layer, dispatching them to the appropriate storage backend(s), and aggregating the results.

### 3.3. Storage Layer

- **Document Store (MongoDB):** Chosen for its flexible, schema-less nature, which allows different plugins to contribute varied metadata without requiring rigid database migrations. It will store the normalized JSON documents.
- **Vector Store (FAISS):** Chosen for its efficiency in performing similarity searches on high-dimensional vectors. It will store the embeddings generated by each plugin, enabling powerful semantic search capabilities.
- **Relational DB (Existing - Postgres):** The existing database will continue to be used for storing structured, relational data such as user accounts, roles, and API keys.

---

## 4. Data Model and Flow

The system hinges on a **Common Metadata Schema**. While the document store is flexible, the `normalize()` method of each plugin must transform its source-specific data into a standardized structure.

**Example Common Metadata Schema:**
```json
{
  "_id": "unique_document_id",
  "source_plugin": "spotify", // Name of the plugin that provided this data
  "source_id": "spotify_track_uri", // The ID within the source system
  "user_id": "user_who_owns_this_data",
  "entity_type": "track", // e.g., 'track', 'album', 'artist'
  "title": "Stairway to Heaven",
  "artist_name": "Led Zeppelin",
  "album_name": "Led Zeppelin IV",
  "release_year": 1971,
  "genres": ["hard rock", "folk rock", "progressive rock"],
  "duration_ms": 482000,
  "media_pointer": {
    "uri": "spotify:track:5CQ30WqJwcep0pYcV4AMNc",
    "url": "https://open.spotify.com/track/5CQ30WqJwcep0pYcV4AMNc"
  },
  "raw_data": { ... } // Optional: store the original, non-normalized data
}
```

**Data Ingestion Flow:**
```
[Plugin: Spotify]          [Plugin: Local Files]
       |                            |
 (raw spotify json)           (id3 tags)
       |                            |
       v                            v
[MetadataService: Ingestion Pipeline]
       |
       +---> [Plugin.normalize()] ---> [Common Schema Document]
       |                                      |
       |                                      v
       |                             [Document Store: MongoDB]
       |
       +---> [Plugin.generate_embeddings()] -> [Vector]
                                               |
                                               v
                                     [Vector Store: FAISS]
```

---

## 5. API Integration

New endpoints will be added under an `/api/metadata` prefix.

- `POST /api/metadata/ingest`: Triggers a full ingestion run for all or specified plugins for the authenticated user.
- `GET /api/metadata/search`: The unified query endpoint.
  - **Structured Query:** `?filter=artist_name:Led Zeppelin AND release_year:>1970`
  - **Semantic Query:** `?q=epic 70s rock ballads`
- `GET /api/metadata/plugins`: Lists all discovered and available metadata plugins.

These endpoints will be protected by the existing Admin API Key authentication and will be integrated with the future RBAC system.

---

## 6. Multi-Tenancy and Security

- **Namespacing:** All documents in MongoDB and all vectors in FAISS will be required to have a `user_id` field. The `MetadataService` will enforce this, ensuring a user's query only ever operates on their own data.
- **RBAC:** A new set of permissions will be defined (e.g., `metadata:read`, `metadata:ingest:{plugin_name}`). The API endpoints will check these permissions before executing an operation. This allows fine-grained control, such as allowing a user to ingest from their local files but not from Spotify.

---

## 7. High-Level Implementation Plan & Roadmap

1.  **Phase 1: Core Service & Storage Setup**
    -   Set up MongoDB and FAISS instances (e.g., in Docker Compose for local dev).
    -   Implement the initial `MetadataService` with plugin discovery logic.
    -   Define the `BaseMetadataProvider` interface and the Common Metadata Schema.

2.  **Phase 2: Refactor Spotify into a Plugin**
    -   Create a new `zotify-spotify-metadata-plugin` package.
    -   Move all relevant logic into it, implementing the `BaseMetadataProvider` interface.
    -   Ensure the `MetadataService` can discover and run the plugin's ingestion pipeline.

3.  **Phase 3: Structured Query Interface**
    -   Implement the `/api/metadata/search` endpoint with support for structured `filter` queries.
    -   The `MetadataService` will be responsible for translating the filter query into a valid MongoDB query.

4.  **Phase 4: Semantic Search & Embeddings**
    -   Implement the `generate_embeddings` logic in the Spotify plugin (e.g., using a pre-trained sentence transformer model on track/album titles).
    -   Integrate the FAISS client into the `MetadataService`.
    -   Extend the `/api/metadata/search` endpoint to handle the `q` parameter for semantic search.

5.  **Phase 5: Multi-Tenancy & API Polish**
    -   Integrate the user namespacing and RBAC checks into all service methods and API endpoints.
    -   Add other helper endpoints (`/plugins`, `/ingest` status, etc.).

### Pseudocode Example

```python
# In MetadataService

async def search(query: str, user: User):
    # 1. Semantic Search (if applicable)
    query_vector = await self.embedding_model.encode(query)
    vector_ids = await self.vector_store.search(vector=query_vector, user_id=user.id, k=50)

    # 2. Structured Search (if applicable)
    # filter_query = parse_structured_filter(query)
    # doc_ids = await self.doc_store.find(filter=filter_query, user_id=user.id)

    # 3. Aggregate and Fetch
    # final_ids = intersect(vector_ids, doc_ids)
    # results = await self.doc_store.get_by_ids(ids=final_ids)
    return results
```

---

## 8. Benefits & Future Proofing

- **Ultimate Extensibility:** The project's core value proposition becomes its ability to unify any data source, not just its implementation of one.
- **Scalability:** Decoupling the components allows the Document Store, Vector Store, and API to be scaled independently.
- **Powerful New Features:** Enables cross-source analysis, discovery of missing media, and rich, semantic search experiences.
- **Community Engagement:** Creates a clear path for community members to contribute new providers without needing deep knowledge of the core API.
- **Future-Ready:** Easily adaptable to new AI models for embedding, new database technologies, and new music sources.
