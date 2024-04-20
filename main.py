import asyncio
import subprocess
import logging
from update_proxies_id import update_proxies_and_user_id


# Configure logging to display on the terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#StreamHandler to log messages to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

async def run_touch_grass():
    try:
        # Run Touch_Grass.py
        process = await asyncio.create_subprocess_exec(
            "python", "Touch_Grass.py",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for 20 minutes and terminate TouchGrass - you can set your own duration
        try:
            await asyncio.wait_for(process.communicate(), timeout=1200)  # in seconds oooo
            logging.info("TouchGrass.py running...")
        except asyncio.TimeoutError:
            logging.error("TouchGrass.py timed out. Terminating...")
            process.terminate()
            await process.wait()

    except Exception as e:
        logging.error(f"Error occurred while running TouchGrass.py: {e}")


async def main():
    while True:
        try:
            logging.info("Running update_proxies_and_user_id.py...")
            # Run update_proxies_and_user_id.py
            update_proxies_and_user_id()
            logging.info("id and proxies updated successfully.")

            logging.info("Running TouchGrass.py...")
            # Run TouchGrass.py with timeout and termination
            await run_touch_grass()

        except Exception as e:
            logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
