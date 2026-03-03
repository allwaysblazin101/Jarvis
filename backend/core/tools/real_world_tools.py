import requests

class RealWorldTools:
    async def get_weather(self, city="Toronto"):
        try:
            r = requests.get(f"https://wttr.in/{city}?format=%C+%t", timeout=5)
            return r.text.strip()
        except:
            return "Weather unavailable"

    async def calculate(self, expression: str):
        try:
            return str(eval(expression, {"__builtins__": {}}, {}))
        except:
            return "Calculation error"
