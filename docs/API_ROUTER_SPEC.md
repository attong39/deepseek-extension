# API Router Spec (v1 & v2)

Goal: Make Copilot/AI generate the correct files for each new resource and keep clean boundaries between app/, core/, data/.

Constraints
- Versioning namespaces: /api/v1/... and /api/v2/... with code in app/api/v1 and app/api/v2
- Thin routers: endpoints only parse/validate input (Pydantic In), depend-inject use-cases/services, return Pydantic Out. No business logic in app/.
- Clear tags, response_model, status codes. Errors use app/exceptions/*.
- REST: GET /{res}, GET /{res}/{id}, POST /{res}, PATCH /{res}/{id}, DELETE /{res}/{id}
- Pagination: page, page_size; sorting/filters via value-objects, not free dicts.

Pattern
- File: app/api/v1/<resource>.py
- Router: APIRouter(prefix="/<resource>", tags=["<resource>"])
- RBAC: dependencies=[Depends(require_permission("resource:action"))] or require_permissions([...])
- DI: use_case=Depends(get_<action>_<resource>_uc)
- Serializers: app/serializers/<resource>_serializers.py with FooCreateIn/FooUpdateIn/FooOut and from_entity/to_vo helpers.

Example
```
from fastapi import APIRouter, Depends
from app.dependencies import get_create_agent_uc
from app.serializers.agent_serializers import AgentCreateIn, AgentOut
from app.middleware.auth import require_permission

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", response_model=AgentOut, status_code=201,
             dependencies=[Depends(require_permission("agent:create"))])
async def create_agent(payload: AgentCreateIn, use_case=Depends(get_create_agent_uc)):
    entity = await use_case(**payload.model_dump())
    return AgentOut.from_entity(entity)
```

Checklist per resource
- app/api/v1/<resource>.py: router with 5 basic REST endpoints
- app/serializers/<resource>_serializers.py: In/Out models with from_entity
- app/validators/<resource>_validators.py: optional extra validation
- core/use_cases/<resource>/: create, get, list, update, delete use-cases
- data/repositories/<resource>_repository.py: repository interface/impl
- app/dependencies.py: get_<action>_<resource>_uc factories and type aliases

Notes
- Keep core pure. app/ may import core and data via DI only. data/ contains persistence and no domain logic.
- Update barrels (__init__.py) when adding modules.
