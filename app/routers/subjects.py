from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.database import edgedb_client

from app.queries.get_subject_async_edgeql import GetSubjectResult, get_subject
from app.queries.get_subjects_async_edgeql import GetSubjectsResult, get_subjects

router = APIRouter()


@router.get("/subjects/")
async def read_subjects(offset: int = 0, limit: int = 10) -> list[GetSubjectsResult]:
    return await get_subjects(edgedb_client, offset=offset, limit=limit)


@router.get("/subject/{subject_id}")
async def read_subject(subject_id: UUID) -> GetSubjectResult:
    subject = await get_subject(edgedb_client, subject_id=subject_id)

    if subject is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return subject