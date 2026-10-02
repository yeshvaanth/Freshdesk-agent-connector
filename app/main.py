from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.tickets import router as tickets_router
from app.exceptions import TicketNotFoundError


app = FastAPI()


@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(
    request: Request,
    exc: TicketNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(tickets_router)