from led_button import ButtonPressed, LedButton
from textual.app import App
from textual.widgets import Placeholder
import asyncio

class FettBox(App):

    async def on_mount(self) -> None:
        self.red_button = LedButton(label="Red Button", name="red_button", color="red", pin=5)
        await self.view.dock(self.red_button, edge="top", )
        asyncio.create_task(self.start())
    
    async def start(self):
        task = asyncio.create_task(self.red_button.start_blink(500))
        await asyncio.sleep(2)
        task.cancel()
        await self.red_button.on()

        task = asyncio.create_task(self.red_button.start_breath(200))
        await asyncio.sleep(2)
        task.cancel()

        # await led.on(80)
        # await asyncio.sleep(2)
        # await led.off()

    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        assert isinstance(message.sender, LedButton)



#asyncio.run(main())
FettBox.run(title="Fett Box", log="textual.log")