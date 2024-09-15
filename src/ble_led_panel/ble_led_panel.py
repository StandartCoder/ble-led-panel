import asyncio
import logger
from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

LOGGER = logger.setup_logger(__name__, logger.logging.DEBUG)

class BLEPanelHandler:
    def __init__(self, address: str):
        """
        Initializes the BLEPanelHandler with the address of the BLE device.

        :param address: The Bluetooth address of the LED matrix
        """
        self.address = address
        self.client = None
        self.uuids = {
            "write": None,
            "notify": None,
        }

    async def search(self):
        """
        Searches for the BLE device with the given address.
        """
        LOGGER.info("Searching for BLE devices...")
        try:
            async with BleakClient(address_or_ble_device=self.address, timeout=10.0) as client:
                try:
                    self.client = client
                    LOGGER.info(f"Found target BLE device: {self.address}")
                    return True
                except Exception as e:
                    LOGGER.warning(f"No BLE device found with address {self.address}... {e}")
                    return False
        except Exception as e:
            LOGGER.warning(f"No BLE device found with address {self.address}")
            return False

    async def connect(self):
        """
        Connects to the BLE device with the given address.
        """
        LOGGER.info(f"Connecting to BLE device with the address: {self.address}")
        try:
            if self.client and self.address:
                await self.client.connect()
                LOGGER.info(f"Connected to BLE device with the address: {self.address}")
            else:
                if not self.client:
                    LOGGER.error("Couldn't connect to BLE device: No client available")
                else:
                    LOGGER.error("Couldn't connect to BLE device: No address given")
        except Exception as e:
            LOGGER.error(f"Failed to connect to BLE device: {e}")

    async def disconnect(self):
        """
        Disconnects from the BLE device.
        """
        LOGGER.info(f"Disconnecting from BLE device with the address: {self.address}")
        try:
            if self.client:
                await self.client.disconnect()
                LOGGER.info(f"Disconnected from BLE device at {self.address}")
            else:
                LOGGER.error("Couldn't disconnect from BLE device: No client available")
        except Exception as e:
            LOGGER.error(f"Failed to disconnect from BLE device: {e}")

    def checkIfConnected(self):
        """
        Checks the connection status with the BLE device.
        """
        try:
            if self.client:
                connected = self.client.is_connected  # Updated to use the property
                LOGGER.debug(f"Connection status with BLE device with the address: {self.address}: {connected}")
                return connected
            else:
                LOGGER.error("No client available to check connection status")
                return False
        except Exception as e:
            LOGGER.error(f"Failed to check connection status: {e}")
            return False

    async def getAndSetCharacteristics(self):
        """
        Retrieves the characteristics of the BLE device.
        """
        try:
            services = self.client.services
            for service in services:
                for characteristic in service.characteristics:
                    if "write" in characteristic.properties:
                        self.uuids["write"] = characteristic.uuid
                    if "notify" in characteristic.properties:
                        self.uuids["notify"] = characteristic.uuid
                if self.uuids["write"] and self.uuids["notify"]:
                    break
            
            LOGGER.debug(f"Characteristics retrieved: {self.uuids}")
            return
        except Exception as e:
            LOGGER.error(f"Failed to retrieve characteristics: {e}")
            return
        

    async def getDeviceInfo(self):
        """
        Retrieves device information such as name, manufacturer, model number, etc.
        """
        LOGGER.debug("Getting device information...")
        device_info = {}

        try:
            # Assuming services have already been retrieved
            services = self.client.services
            device_info_service = None
            
            # Search for the Device Information Service (UUID: 0x180A)
            for service in services:
                if service.uuid == "0000180a-0000-1000-8000-00805f9b34fb":
                    device_info_service = service
                    break

            if device_info_service:
                for characteristic in device_info_service.characteristics:
                    # Device Name (0x2A29), Manufacturer (0x2A24), Model (0x2A25), etc.
                    if characteristic.uuid == "00002a29-0000-1000-8000-00805f9b34fb":
                        device_info['manufacturer'] = await self.client.read_gatt_char(characteristic.uuid)
                    if characteristic.uuid == "00002a24-0000-1000-8000-00805f9b34fb":
                        device_info['model'] = await self.client.read_gatt_char(characteristic.uuid)
                    if characteristic.uuid == "00002a25-0000-1000-8000-00805f9b34fb":
                        device_info['serial_number'] = await self.client.read_gatt_char(characteristic.uuid)
                    if characteristic.uuid == "00002a00-0000-1000-8000-00805f9b34fb":
                        device_info['device_name'] = await self.client.read_gatt_char(characteristic.uuid)

                LOGGER.debug(f"Device Information retrieved: {device_info}")
            else:
                LOGGER.warning("Device Information Service not found.")

        except Exception as e:
            LOGGER.error(f"Failed to retrieve device information: {e}")
        
        return device_info