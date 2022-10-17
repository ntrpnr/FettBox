from led import Led
from textual.app import App
from textual.widgets import Placeholder
import asyncio

class FettBox(App):

    async def on_mount(self) -> None:
        self.led_red = Led(color="red", pin=5)
        self.led_red.has_edge = False
        await self.view.dock(self.led_red, edge="top", )
        asyncio.create_task(self.start())
    
    async def start(self):
        task = asyncio.create_task(self.led_red.start_blink(500))
        await asyncio.sleep(2)
        task.cancel()
        await self.led_red.off()

        task = asyncio.create_task(self.led_red.start_breath(200))
        await asyncio.sleep(2)
        task.cancel()

        # await led.on(80)
        # await asyncio.sleep(2)
        # await led.off()



#asyncio.run(main())
FettBox.run(title="Fett Box", log="textual.log")