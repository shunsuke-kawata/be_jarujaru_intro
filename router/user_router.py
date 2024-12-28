import sys
sys.path.append('../')
import config
from fastapi import APIRouter, HTTPException,status,Query
import json
from fastapi.responses import JSONResponse