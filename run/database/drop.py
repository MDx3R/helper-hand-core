import asyncio
from infrastructure.app.app import App
from infrastructure.database.models import Base


async def main():
    app = App()
    await app.database.drop_database(Base.metadata)


if __name__ == "__main__":
    asyncio.run(main())
