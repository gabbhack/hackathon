# AUTOGENERATED FROM 'app/queries/add_subject.edgeql' WITH:
#     $ edgedb-py -I hackathon --tls-security insecure --skip-pydantic-validation


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
class AddSubjectResult(NoPydanticValidation):
    id: uuid.UUID


async def add_subject(
    executor: edgedb.AsyncIOExecutor,
    *,
    object_key: str,
    number: int,
    type: str,
    subtype: str,
) -> AddSubjectResult | None:
    return await executor.query_single(
        """\
        insert Subject {
          obj_key := <str>$object_key,
          number := <int64>$number,
          type := <str>$type,
          subtype := <str>$subtype
        } unless conflict on .obj_key\
        """,
        object_key=object_key,
        number=number,
        type=type,
        subtype=subtype,
    )