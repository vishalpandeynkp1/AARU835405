import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from RessoMusic import LOGGER, app, userbot
from RessoMusic.core.call import AMBOTOP
from RessoMusic.misc import sudo
from RessoMusic.plugins import ALL_MODULES
from RessoMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Check if all client variables are set
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()  # Ensure sudo privileges
    
    # Get banned users and add them to BANNED_USERS
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Error fetching banned users: {e}")

    # Start the main bot app
    await app.start()

    # Import all plugins
    for all_module in ALL_MODULES:
        importlib.import_module("RessoMusic.plugins" + all_module)
    LOGGER("RessoMusic.plugins").info("Successfully Imported Modules...")

    # Start userbot and AMBOTOP
    await userbot.start()
    await AMBOTOP.start()

    try:
        # Stream the intro video
        await AMBOTOP.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("RessoMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except Exception as e:
        LOGGER("RessoMusic").warning(f"Error streaming video: {e}")

    # Start the decorator functions
    await AMBOTOP.decorators()
    LOGGER("RessoMusic").info("Resso Music Bot Started")

    # Wait for idle state
    await idle()

    # Stop the app and userbot
    await app.stop()
    await userbot.stop()
    LOGGER("RessoMusic").info("Stopping AMBOTOP Music Bot...")


# Main entry point
if __name__ == "__main__":
    asyncio.run(init())  # Use asyncio.run() to run the main function
