import math

class EquationSolver:
    def __init__(self, expression):
        self.expression = expression

    def _function(self, x):
        try:
            return eval(self.expression, {'x': x, 'math': math})
        except (NameError, TypeError):
            raise ValueError("Invalid expression or variable name. Use 'x' as the variable.")

    def _derivative(self, func, x, h=1e-7):  # Numerical derivative using the central difference method
        return (func(x + h) - func(x - h)) / (2 * h)

def comparison(expression, interval, tolerance=1e-7, max_iterations=100):
    
    solver = EquationSolver(expression)
    f = solver._function

    # Initialize results
    bisection_result = None
    newton_result = None
    bisection_steps = None
    newton_raphson_steps = None

    # Bisection Method
    a, b = interval
    if f(a) * f(b) >= 0:
        print("Error: f(a) and f(b) must have opposite signs for the bisection method.")
    else:
        bisection_steps = 0
        while (b - a) / 2 > tolerance and bisection_steps < max_iterations:
            c = (a + b) / 2
            if f(c) == 0:
                bisection_result = c
                break
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
            bisection_steps += 1
        bisection_result = (a + b) / 2  # Final approximation
        if bisection_steps == max_iterations:
            print("Bisection method did not converge within the maximum iterations.")

    # Newton-Raphson Method
    initial_guess = (interval[0] + interval[1]) / 2  # Using the midpoint as a reasonable starting point
    newton_raphson_steps = 0
    x = initial_guess
    try:
        while abs(f(x)) > tolerance and newton_raphson_steps < max_iterations:
            df_dx = solver._derivative(f, x)
            if df_dx == 0:
                print("Error: Derivative is zero in Newton-Raphson method. Cannot proceed.")
                newton_raphson_steps = None
                break
            x_new = x - f(x) / df_dx
            x = x_new
            newton_raphson_steps += 1
        newton_result = x
        if newton_raphson_steps is not None and newton_raphson_steps == max_iterations:
            print("Newton-Raphson method did not converge within the maximum iterations.")
    except ValueError as e:
        print(f"Error in Newton-Raphson: {e}")
    except ZeroDivisionError:
        print("Error: Division by zero encountered in Newton-Raphson (likely zero derivative).")

    return {
        'bisection': {
            'root': bisection_result,
            'steps': bisection_steps
        },
        'newton': {
            'root': newton_result,
            'steps': newton_raphson_steps
        }
    }

if __name__ == "__main__":
    equation = input("Enter the equation in terms of 'x' (e.g., x**3 - 2*x - 5): ")
    try:
        lower_bound = float(input("Enter the lower bound of the interval: "))
        upper_bound = float(input("Enter the upper bound of the interval: "))
        tolerance = float(input("Enter the desired tolerance: "))

        results = comparison(
            equation, (lower_bound, upper_bound), tolerance
        )

        print("\nResults:")
        print(f"Bisection Method:")
        if results['bisection']['root'] is not None:
            print(f"  Root: {results['bisection']['root']:.10f}")
            print(f"  Steps: {results['bisection']['steps']}")
        else:
            print("  Did not converge or encountered an error.")

        print(f"\nNewton-Raphson Method:")
        if results['newton']['root'] is not None:
            print(f"  Root: {results['newton']['root']:.10f}")
            print(f"  Steps: {results['newton']['steps']}")
        else:
            print("  Did not converge or encountered an error.")

        if (results['bisection']['root'] is not None and 
            results['newton']['root'] is not None):
            print("\nComparison:")
            if results['newton']['steps'] < results['bisection']['steps']:
                print("Newton-Raphson was faster in this case.")
            elif results['newton']['steps'] > results['bisection']['steps']:
                print("Bisection was faster in this case.")
            else:
                print("Both methods took the same number of steps.")

    except ValueError:
        print("Invalid input. Please enter numeric values for the interval and tolerance.")