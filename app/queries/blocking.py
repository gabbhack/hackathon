# AUTOGENERATED FROM:
#     'app/queries/add_file.edgeql'
#     'app/queries/add_subject.edgeql'
#     'app/queries/add_task.edgeql'
#     'app/queries/add_token.edgeql'
#     'app/queries/add_user.edgeql'
#     'app/queries/delete_token.edgeql'
#     'app/queries/get_subject.edgeql'
#     'app/queries/get_subjects.edgeql'
#     'app/queries/get_tasks.edgeql'
#     'app/queries/get_user_by_auth_data.edgeql'
#     'app/queries/get_user_by_token.edgeql'
#     'app/queries/search_by_obj_key.edgeql'
# WITH:
#     $ edgedb-py -I hackathon --tls-security insecure --skip-pydantic-validation --target blocking --file app/queries/blocking.py


from __future__ import annotations
import dataclasses
import datetime
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
class AddFileResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class AddSubjectResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class AddTaskResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class AddTokenResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class AddUserResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class GetSubjectResult(NoPydanticValidation):
    created: datetime.datetime | None
    id: uuid.UUID
    modified: datetime.datetime | None
    obj_key: str
    state: str | None
    general_contractor: str | None
    general_designer_key: str | None
    number_of_workers: int | None
    square: str | None
    subtype: str | None
    type: str | None
    number: int | None


@dataclasses.dataclass
class GetTasksResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    code: str
    predicted_end_date: datetime.date | None
    actual_end_date: datetime.date | None
    reasons: list[GetTasksResultReasonsItem]


@dataclasses.dataclass
class GetTasksResultReasonsItem(NoPydanticValidation):
    id: uuid.UUID
    name: str
    about: str


@dataclasses.dataclass
class GetUserByTokenResult(NoPydanticValidation):
    id: uuid.UUID
    token: str


def add_file(
    executor: edgedb.Executor,
    *,
    user_id: uuid.UUID,
    origin_filename: str,
    obj_key: str | None,
) -> AddFileResult:
    return executor.query_single(
        """\
        insert File {
          owner := (
            select User
            filter .id = <uuid>$user_id
          ),
          origin_filename := <str>$origin_filename,
          obj_key := <optional str>$obj_key
        }\
        """,
        user_id=user_id,
        origin_filename=origin_filename,
        obj_key=obj_key,
    )


def add_subject(
    executor: edgedb.Executor,
    *,
    object_key: str,
    number: int,
    type: str,
    subtype: str,
) -> AddSubjectResult | None:
    return executor.query_single(
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


def add_task(
    executor: edgedb.Executor,
    *,
    obj_key: str,
    name: str,
    code: str,
    predicted_end_date: datetime.date | None,
    actual_end_date: datetime.date | None,
) -> AddTaskResult:
    return executor.query_single(
        """\
        insert Task {
          subject := (
            select Subject
            filter .obj_key = <str>$obj_key
          ),
          name := <str>$name,
          code := <str>$code,
          predicted_end_date := <optional cal::local_date>$predicted_end_date,
          actual_end_date := <optional cal::local_date>$actual_end_date
        } unless conflict on ((.subject, .code)) else (
          update Task set {
            predicted_end_date := <optional cal::local_date>$predicted_end_date,
            actual_end_date := <optional cal::local_date>$actual_end_date
          }
        )\
        """,
        obj_key=obj_key,
        name=name,
        code=code,
        predicted_end_date=predicted_end_date,
        actual_end_date=actual_end_date,
    )


def add_token(
    executor: edgedb.Executor,
    *,
    user_id: uuid.UUID,
    token: str,
) -> AddTokenResult:
    return executor.query_single(
        """\
        insert Token {
          owner := (
            select User
            filter .id = <uuid>$user_id
          ),
          value := <str>$token
        }\
        """,
        user_id=user_id,
        token=token,
    )


def add_user(
    executor: edgedb.Executor,
    *,
    login: str,
    password_hash: str,
) -> AddUserResult:
    return executor.query_single(
        """\
        insert User {
          login := <str>$login,
          password_hash := <str>$password_hash
        }\
        """,
        login=login,
        password_hash=password_hash,
    )


def delete_token(
    executor: edgedb.Executor,
    *,
    token: str,
) -> AddTokenResult | None:
    return executor.query_single(
        """\
        delete Token filter .value = <str>$token\
        """,
        token=token,
    )


def get_subject(
    executor: edgedb.Executor,
    *,
    subject_id: uuid.UUID,
) -> GetSubjectResult | None:
    return executor.query_single(
        """\
        select Subject{*} filter .id = <uuid>$subject_id limit 1\
        """,
        subject_id=subject_id,
    )


def get_subjects(
    executor: edgedb.Executor,
    *,
    offset: int | None,
    limit: int | None,
) -> list[GetSubjectResult]:
    return executor.query(
        """\
        select Subject{*} offset <optional int64>$offset limit <optional int64>$limit\
        """,
        offset=offset,
        limit=limit,
    )


def get_tasks(
    executor: edgedb.Executor,
    *,
    subject_id: uuid.UUID,
) -> list[GetTasksResult]:
    return executor.query(
        """\
        select Task {
          name,
          code,
          predicted_end_date,
          actual_end_date,
          reasons: {
            name,
            about
          }
        }
        filter .subject.id = <uuid>$subject_id\
        """,
        subject_id=subject_id,
    )


def get_user_by_auth_data(
    executor: edgedb.Executor,
    *,
    login: str,
    password_hash: str,
) -> AddUserResult | None:
    return executor.query_single(
        """\
        select User filter .login = <str>$login and .password_hash = <str>$password_hash limit 1\
        """,
        login=login,
        password_hash=password_hash,
    )


def get_user_by_token(
    executor: edgedb.Executor,
    *,
    token: str,
) -> GetUserByTokenResult | None:
    return executor.query_single(
        """\
        select User {id, token := <str>$token} filter .tokens.value = <str>$token limit 1\
        """,
        token=token,
    )


def search_by_obj_key(
    executor: edgedb.Executor,
    *,
    obj_key: str,
) -> list[GetSubjectResult]:
    return executor.query(
        """\
        select Subject{*} filter .obj_key like <str>$obj_key ++ '%'\
        """,
        obj_key=obj_key,
    )
