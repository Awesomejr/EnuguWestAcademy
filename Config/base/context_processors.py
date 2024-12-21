import datetime
from base.models import Session


def siteName(request) -> str:
    return {"site_name": "Enugu West Academy™"}

def getCurrentYear(request) -> str:
    current_year = datetime.datetime.today().year
    return {"current_year": current_year}

def getCurrentMonth(request) -> str:
    current_month = datetime.datetime.today().month
    return {"current_month": current_month}

def sessionContext(request) -> object:
    session = Session.objects.latest("created_on")
    return {"session": session}