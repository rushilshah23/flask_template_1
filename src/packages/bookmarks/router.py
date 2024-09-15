from flask import Blueprint, request


router = Blueprint("bookmarks",__name__)


@router.get("/")
def index():
    return "user authenticated"


@router.post("/register")
def register():
    return "User registered !"

@router.post("/login")
def login():
    return "User logged in !"