import math

class NRI:#gets a math expression using x as the variable and computes its numerical deriivative
    def __init__(self, expression, tolerance=pow(10, -10), initial_guess= 1.0): #creating an instance in the class, and sets tolerance levels for convergence
        #also presets the initial guess to 1.0
        self.expression = expression
        self.h = tolerance
        self.initial_guess = initial_guess
        self.allowed_names = {
            'math': math,
            'sin':math.sin,
            'cos':math.cos,
            'exp':math.exp,
            'log':math.log,
            'pi':math.pi,
            'e':math.e
        }
#thnis part maps inputs functions like sine cosine to corresponding modules in the math library
    def __function(self, x):
        return float(eval(self.expression,self.allowed_names,{'x':x}))

    def __function_derivative(self, x):
        return (self.__function(x + self.h) - self.__function(x)) / self.h#approximate derivative by forward or finite difference method

    def __numerical_scheme(self, x):
        return f"{x}  -  {self.__function(x)} / {self.__function_derivative(x)}"#

    def __print_details(self):
        print(f"f(x) = {self.expression}")
        print(f"x0 = {self.initial_guess}")
        print(
            f"---------------------------------------------------------------------------------------------------------------------------")

    def solve(self):
        x = self.initial_guess
        i = 0  # counter
        self.__print_details()
        while abs(self.__function(x)) > self.h:
            x = x - self.__function(x) / self.__function_derivative(x)
            print(f"x{i} = {self.__numerical_scheme(x)} = {x}")
            print(f"f(x{i}) = {self.__function(x)}", end="\n\n")
            i += 1


print("NEWTON RAPHSONS ITERATOR")
expression = input("Input expression into the equation in the form f(x) = 0: ")
print(
    f"---------------------------------------------------------------------------------------------------------------------------")
solver = NRI(expression)
solver.solve()