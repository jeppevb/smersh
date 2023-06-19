import logging 
from fastapi import APIRouter
from .models import Subject, Vote


log = logging.getLogger(__name__)

router = APIRouter()


