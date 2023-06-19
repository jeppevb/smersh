import logging 
from fastapi import APIRouter
from .models import Subject, Vote
from .schemas import Subject as DtoSubject, Vote as DtoVote
from .service import get_subjects

log = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "",
    response_model=List[Subject],
    summary="Retrieves a list of subjects.",
)
def get_subjects(db_session: DbSession):
    """Retrieves a list of subjects."""
    return current_case

