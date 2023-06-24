# AUTOGENERATED FROM 'app/queries/add_user.edgeql' WITH:
#     $ edgedb-py --skip-pydantic-validation


from __future__ import annotations
import dataclasses
import edgedb
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass

        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class AddUserResult(NoPydanticValidation):
    id: uuid.UUID


async def add_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    login: str,
    password_hash: str,
) -> AddUserResult:
    return await executor.query_single(
        """\
        insert User {
          login := <str>$login,
          password_hash := <str>$password_hash
        }\
        """,
        login=login,
        password_hash=password_hash,
    )
