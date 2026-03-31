"""
JARVIS Calculator — math expressions + unit conversion
"""
import re
import math


class SmartCalculator:

    def calculate(self, expression: str) -> str:
        """Evaluate a mathematical expression safely"""
        try:
            # Clean the expression
            expr = expression.strip()
            # Remove common words
            for w in ["calculate", "calc", "math", "what is", "what's", "="]:
                expr = expr.replace(w, "").strip()

            if not expr:
                return "Please provide a mathematical expression, sir."

            # Replace ^ with **
            expr = expr.replace("^", "**")
            # Replace × with *
            expr = expr.replace("×", "*").replace("÷", "/").replace("x", "*")

            # Safe evaluation with math functions
            allowed = {
                "__builtins__": {},
                "abs": abs, "round": round, "pow": pow,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "log2": math.log2, "pi": math.pi, "e": math.e,
                "ceil": math.ceil, "floor": math.floor,
                "factorial": math.factorial,
            }
            result = eval(expr, allowed)

            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 6)
            return f"The result of {expression.strip()} = {result}, sir."
        except ZeroDivisionError:
            return "Division by zero is undefined, sir. Even I cannot compute the impossible."
        except Exception as e:
            return f"I couldn't evaluate that expression, sir. Please check the syntax. ({e})"

    def convert(self, text: str) -> str:
        """Convert units"""
        text = text.lower().strip()
        for w in ["convert", "what is", "how many", "how much"]:
            text = text.replace(w, "").strip()

        # Extract: number + from_unit to to_unit
        pattern = r"([\d.]+)\s*(\w+)\s+(?:to|in|into)\s+(\w+)"
        m = re.search(pattern, text)
        if not m:
            # Try without number
            pattern2 = r"(\w+)\s+(?:to|in|into)\s+(\w+)"
            m2 = re.search(pattern2, text)
            if m2:
                return self._convert(1, m2.group(1), m2.group(2))
            return "I couldn't parse that conversion, sir. Example: 'convert 5 km to miles'."

        value = float(m.group(1))
        from_unit = m.group(2)
        to_unit = m.group(3)
        return self._convert(value, from_unit, to_unit)

    def _convert(self, value: float, from_unit: str, to_unit: str) -> str:
        conversions = {
            # Length
            ("km", "miles"): 0.621371, ("miles", "km"): 1.60934,
            ("km", "meters"): 1000, ("meters", "km"): 0.001,
            ("meters", "feet"): 3.28084, ("feet", "meters"): 0.3048,
            ("meters", "cm"): 100, ("cm", "meters"): 0.01,
            ("cm", "inches"): 0.393701, ("inches", "cm"): 2.54,
            ("feet", "inches"): 12, ("inches", "feet"): 1/12,
            ("miles", "feet"): 5280, ("feet", "miles"): 1/5280,
            # Weight
            ("kg", "pounds"): 2.20462, ("pounds", "kg"): 0.453592,
            ("kg", "grams"): 1000, ("grams", "kg"): 0.001,
            ("grams", "mg"): 1000, ("mg", "grams"): 0.001,
            ("kg", "oz"): 35.274, ("oz", "kg"): 0.0283495,
            ("tons", "kg"): 1000, ("kg", "tons"): 0.001,
            # Temperature handled separately
            # Speed
            ("kmh", "mph"): 0.621371, ("mph", "kmh"): 1.60934,
            ("mps", "kmh"): 3.6, ("kmh", "mps"): 0.27778,
            # Area
            ("sqm", "sqft"): 10.7639, ("sqft", "sqm"): 0.092903,
            ("hectares", "acres"): 2.47105, ("acres", "hectares"): 0.404686,
            # Volume
            ("liters", "gallons"): 0.264172, ("gallons", "liters"): 3.78541,
            ("ml", "liters"): 0.001, ("liters", "ml"): 1000,
            # Data
            ("kb", "mb"): 0.001, ("mb", "kb"): 1000,
            ("mb", "gb"): 0.001, ("gb", "mb"): 1000,
            ("gb", "tb"): 0.001, ("tb", "gb"): 1000,
            ("bytes", "kb"): 0.001, ("kb", "bytes"): 1000,
        }

        # Normalize aliases
        aliases = {
            "kilometer": "km", "kilometers": "km", "kilometre": "km",
            "mile": "miles", "meter": "meters", "metre": "meters",
            "foot": "feet", "inch": "inches", "centimeter": "cm", "centimeters": "cm",
            "kilogram": "kg", "kilograms": "kg", "gram": "grams", "pound": "pounds", "lb": "pounds", "lbs": "pounds",
            "ounce": "oz", "ounces": "oz",
            "celsius": "c", "centigrade": "c", "fahrenheit": "f",
            "kelvin": "k", "liter": "liters", "litre": "liters", "litres": "liters",
            "gallon": "gallons", "milliliter": "ml", "millilitre": "ml",
            "megabyte": "mb", "gigabyte": "gb", "kilobyte": "kb", "terabyte": "tb",
        }
        fu = aliases.get(from_unit, from_unit)
        tu = aliases.get(to_unit, to_unit)

        # Temperature conversions
        if fu == "c" and tu == "f":
            result = (value * 9/5) + 32
            return f"{value}°C = {result:.2f}°F, sir."
        if fu == "f" and tu == "c":
            result = (value - 32) * 5/9
            return f"{value}°F = {result:.2f}°C, sir."
        if fu == "c" and tu == "k":
            result = value + 273.15
            return f"{value}°C = {result:.2f}K, sir."
        if fu == "k" and tu == "c":
            result = value - 273.15
            return f"{value}K = {result:.2f}°C, sir."
        if fu == "f" and tu == "k":
            result = (value - 32) * 5/9 + 273.15
            return f"{value}°F = {result:.2f}K, sir."

        key = (fu, tu)
        if key in conversions:
            result = value * conversions[key]
            return f"{value} {from_unit} = {result:.4f} {to_unit}, sir."

        return f"I don't know how to convert {from_unit} to {to_unit}, sir. Supported: length, weight, temperature, speed, volume, data."


smart_calculator = SmartCalculator()
