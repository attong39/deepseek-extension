from __future__ import annotations

import strawberry
from strawberry.fastapi import GraphQLRouter

from .schema.base import Mutation, Query, Subscription

"""GraphQL application setup and configuration."""
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
graphql_router = GraphQLRouter(schema, path="/graphql", graphiql=True)
__all__ = [
    "graphql_router",
    "schema",
]
