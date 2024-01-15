import os
import sys
import importlib
import FilterGui as gui

def main(signal):

    #Opens gui for inputs
    file_name, function_name = gui.show()

    arg1 = signal #Argument for function

    result = run_function_from_file(file_name, function_name, arg1)
    print(f"Result: {result}")
    return signal, result

#This function runs a function from a new specified file in the systsem.
#The parameters are the file name of the python file with the filters,
#the name of the function that is mainly called, the arguments
#for the function and the kwargs.
#The return is the return of the filter function.
def run_function_from_file(file_name, function_name, *args, **kwargs):
    if os.path.exists(file_name) != True:
        print(f"Error: File '{file_name}' not found.")
        return

    try:
        new_string = file_name.split('/')
        temp_string = new_string[len(new_string)-1]
        name = temp_string.split(".")
        spec = importlib.util.spec_from_file_location(function_name, file_name)
        # Import the module dynamically
        module = importlib.util.module_from_spec(spec)
        sys.modules[function_name] = module
        spec.loader.exec_module(module) 
    except ModuleNotFoundError as e:
        print(f"Error: Module '{file_name}' not found.")
        print(e)
        return

    # Get the function dynamically
    target_function = getattr(module, function_name, None)

    if target_function is not None and callable(target_function):
        # Execute the function with provided arguments and keyword arguments
        result = target_function(*args, **kwargs)
        return result
    else:
        print(f"Error: Function '{function_name}' not found in module '{file_name}'.")
        return