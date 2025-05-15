from application.transactions.configuration import set_transaction_manager
from core.config import Config
from core.containers import Container
from infrastructure.database.database import Database
from infrastructure.database.models import Base
from infrastructure.fastapi.server.server import FastAPIServer


class App:
    def __init__(self) -> None:
        self.container = Container()
        self.container.init_resources()
        self.config = self.container.config()

        self.database = Database(self.config.db)
        self.server = FastAPIServer()

    def configure(self):
        set_transaction_manager(self.container.transaction_manager())
        self.server.on_start_up(
            self.database.create_database, metadata=Base.metadata
        )
        self.server.on_tear_down(self.database.shutdown)

        self.server.setup_routes()
        self.server.include_middlewares()
        self.server.include_exception_handlers()

    def run(self):
        import uvicorn

        uvicorn.run(self.server.app, host="0.0.0.0", port=8000)

    def get_server(self):
        return self.server.app
