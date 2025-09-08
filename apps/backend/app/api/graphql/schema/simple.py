from __future__ import annotations

"""Simple GraphQL schema SDL for One-Click Learning."""
SCHEMA_SDL = """
type RagHit {
    doc_id: ID!
    chunk_idx: Int!
    text: String!
    score: Float!
}
type Query {
    ragSearch(q: String!, topK: Int = 5): [RagHit!]!
}
type Mutation {
    ingestText(source: String!, text: String!): Int!
}
type Subscription {
    trainingProgress: Int!
}
"""
__all__ = [
    "SCHEMA_SDL",
]
