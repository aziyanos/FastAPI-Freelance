import time
import logging
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

# Настроим логгер
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()


# Middleware для логирования
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    # Логируем входящий запрос (включая query параметры)
    logger.info(f"➡️  {request.method} {request.url}")

    try:
        # Передаем управление следующему middleware или обработчику
        response = await call_next(request)
    except Exception as exc:
        # Логируем ошибку, если возникла
        logger.exception(f"❌ Error during request {request.method} {request.url}")
        raise exc

    # Измеряем время обработки
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

    # Логируем исходящий ответ
    status_emoji = "👍" if response.status_code < 400 else "❌"
    logger.info(
        f"{status_emoji} {request.method} {request.url.path} - "
        f"Status: {response.status_code} - {process_time:.2f} ms"
    )

    return response