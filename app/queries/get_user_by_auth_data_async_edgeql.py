# AUTOGENERATED FROM 'app/queries/get_user_by_auth_data.edgeql' WITH:
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
class GetUserByAuthDataResult(NoPydanticValidation):
    id: uuid.UUID


async def get_user_by_auth_data(
    executor: edgedb.AsyncIOExecutor,
    *,
    login: str,
    password_hash: str,
) -> GetUserByAuthDataResult | None:
    return await executor.query_single(
        """\
        select User filter .login = <str>$login and .password_hash = <str>$password_hash limit 1\
        """,
        login=login,
        password_hash=password_hash,
    )
