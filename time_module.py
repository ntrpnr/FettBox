from textual.widget import Widget
from rich.style import Style
from rich.panel import Panel

class TimeModule(Widget):
    def __init__(self, name: str, color, led_pin, button_pin):
        self.name = name
        self.color = color
        self.led_pin = led_pin
        self.button_pin = button_pin
        super().__init__(name = name)

    def render(self) -> Panel:
        return Panel( border_style=Style(color="black"))