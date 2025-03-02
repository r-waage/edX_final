#Assign functions to variables
print("Assign functions to variables:")
def plus_one(number):
    return number + 1

add_one = plus_one
result = add_one(5)
print(f"Assign function plus_one to function add_on and call add_on(5), this shoule add 1 so 6 should be the result: {result}")

#Defining functions Inside other functions
print("Defining functions Inside other functions")
def plus_one2(number):
    def add_one2(number):
        return number + 1


    result = add_one2(number)
    return result
result2=plus_one2(4)
print(f"Functions insight other Functions, results should be again 6: {result2}")

#Taking functions as Argument of functions
def plus_one3(number):
    return number + 1

def function_call(function):
    number_to_add = 5
    return function(number_to_add)

result3 = function_call(plus_one3)
print(f"Taking functions as argument of other functions, again 6 should be the result: {result3}")


#Functions returning other functions
def hello_function():
    def say_hi():
        return "Hi"
    return say_hi
hello = hello_function()
result4=hello()
print(f"Functions returning other functions: {result4}")

#Understanding the concept of closure functions, i.e. nested functions
#can access the outer scope of the enclosing function.
def outer_function(message):
    def inner_function():
        print(f"Message from closure: {message}")
    return inner_function

closure_function = outer_function("Hello, closures!")
closure_function()
# Output: Message from closure: Hello, closures

#A simple decorator function
def simple_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")
    return wrapper

@simple_decorator
def greet():
    print("Hello!")

greet()

# Output:
# Before the function call
# Hello!
# After the function call
