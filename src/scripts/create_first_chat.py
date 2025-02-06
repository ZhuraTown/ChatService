import click
from sqlalchemy import select

from common.enums import ChatType
from db.database import db
from db.orm import Chat
from scripts.base import make_sync


@click.command(help="Hello World", name='create-first-chat')
@make_sync
async def create_first_chat(

):
    click.echo("Start script")
    async with db.session() as session:
        found_chat = await session.scalar(
                select(Chat).where(
                    Chat.id == 1, Chat.deleted_at.is_(None),
                )
        )
        if found_chat:
            click.echo("First chat already exist")
            return

        click.echo("Create first chat")
        session.add(
            Chat(name="General", type=ChatType.GROUP, about="First chat for all users")
        )
        await session.commit()
    click.echo("Finish script")



