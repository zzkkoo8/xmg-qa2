from pathlib import Path

import yaml

from xmg_qa2.api.app import create_app
from xmg_qa2.infrastructure.db.base import make_engine, make_session_factory


def test_generated_openapi_contains_frozen_operations() -> None:
    frozen = yaml.safe_load(Path("specs/003-support-foundation/contracts/openapi.yaml").read_text())
    app = create_app(make_session_factory(make_engine()), [], "schema-only-secret")
    generated = app.openapi()
    for path, methods in frozen["paths"].items():
        generated_path = generated["paths"][f"/api/v1{path}"]
        for method, operation in methods.items():
            assert generated_path[method]["operationId"] == operation["operationId"]
