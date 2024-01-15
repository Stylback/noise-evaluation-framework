import os
import importlib
import copy

def main(signal):
    directory = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(directory, 'TestFilter')
    file_name = os.path.join(directory, 'FiltersLow.py') # Replace with your Python file name
    function_name1 = "main"  # Replace with your function name

    copySignal = copy.deepcopy(signal)
    arg1 = copySignal #Argument for function

    result = run_function_from_file(file_name, function_name1, arg1)
    #print(f"Result: {result}")
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
        new_string = file_name.split(os.sep)
        temp_string = new_string[len(new_string)-1]
        name = temp_string.split(".")
        full_name = ".TestFilter."+ name[0] #The first dot is to note that function is called from a file in the previus folder
        # Import the module dynamically
        module = importlib.import_module(full_name, package=__package__) 
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