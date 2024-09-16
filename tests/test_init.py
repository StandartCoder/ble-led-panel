import asyncio
import ble_led_panel
from ble_led_panel import logger, BLEPanelHandler

LOGGER = logger.setup_logger(__name__)

async def run() -> None:
    # Initialize the BLE panel handler class
    panel = BLEPanelHandler("0CCF7211-8818-5CE3-5257-D7FC2B5B542F")

    # Search for the BLE device
    if not await panel.search():
        return
    
    # Connect to the BLE device, but check if already connected
    if not panel.checkIfConnected():
        await panel.connect()

    # Check if the connection was successful
    if not panel.checkIfConnected():
        return
    
    # Get the device information and characteristics
    await panel.getAndSetCharacteristics()

    # Initialize the LED panel
    LOGGER.info("LED panel initialized successfully")

if __name__ == "__main__":
    asyncio.run(run())