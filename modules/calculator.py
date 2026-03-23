"""
Smart Calculator Module
Math expressions, unit conversions
"""

import re
import math

class SmartCalculator:
    """Advanced calculator with unit conversions"""

    def __init__(self):
        self.safe_functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
            'abs': abs, 'round': round, 'pow': pow,
            'pi': math.pi, 'e': math.e,
            'floor': math.floor, 'ceil': math.ceil,
        }

        self.conversions = {
            ('km', 'miles'): 0.621371,
            ('miles', 'km'): 1.60934,
            ('celsius', 'fahrenheit'): lambda c: c * 9/5 + 32,
            ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9,
            ('kg', 'pounds'): 2.20462,
            ('pounds', 'kg'): 0.453592,
            ('meters', 'feet'): 3.28084,
            ('feet', 'meters'): 0.3048,
            ('cm', 'inches'): 0.393701,
            ('inches', 'cm'): 2.54,
            ('liters', 'gallons'): 0.264172,
            ('gallons', 'liters'): 3.78541,
            ('grams', 'ounces'): 0.035274,
            ('ounces', 'grams'): 28.3495,
        }

    def calculate(self, expression: str) -> str:
        """Safely evaluate a math expression"""
        try:
            # Clean up
            expr = expression.strip()
            expr = expr.replace('^', '**')
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')

            # Validate - only allow safe characters
            if not re.match(r'^[\d\s\+\-\*/\.\(\)\%\*]+$', expr.replace('pi', '').replace('e', '').replace('sqrt', '').replace('sin', '').replace('cos', '').replace('tan', '').replace('log', '').replace('abs', '').replace('round', '').replace('pow', '').replace('floor', '').replace('ceil', '')):
                return f"🔢 Invalid expression. Please use numbers and operators (+, -, *, /, ^, %)"

            # Evaluate safely
            result = eval(expr, {"__builtins__": {}}, self.safe_functions)

            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 6)

            return f"🔢 {expression} = **{result}**"

        except ZeroDivisionError:
            return "🔢 Error: Division by zero"
        except Exception as e:
            return f"🔢 Error calculating: {e}"

    def convert(self, command: str) -> str:
        """Handle unit conversion from natural language"""
        try:
            # Try to parse "convert X unit1 to unit2"
            patterns = [
                r'(\d+\.?\d*)\s*(\w+)\s+(?:to|in)\s+(\w+)',
                r'convert\s+(\d+\.?\d*)\s*(\w+)\s+(?:to|in)\s+(\w+)',
            ]

            for pattern in patterns:
                match = re.search(pattern, command.lower())
                if match:
                    value = float(match.group(1))
                    from_unit = match.group(2).lower()
                    to_unit = match.group(3).lower()

                    key = (from_unit, to_unit)
                    if key in self.conversions:
                        factor = self.conversions[key]
                        if callable(factor):
                            result = factor(value)
                        else:
                            result = value * factor
                        result = round(result, 4)
                        return f"🔄 {value} {from_unit} = **{result} {to_unit}**"

                    return f"🔄 Sorry, I can't convert {from_unit} to {to_unit}. Supported: km/miles, celsius/fahrenheit, kg/pounds, meters/feet, cm/inches, liters/gallons"

            return "🔄 Please specify: convert [value] [unit] to [unit]. Example: convert 10 km to miles"

        except Exception as e:
            return f"🔄 Conversion error: {e}"

smart_calculator = SmartCalculator()
