# from Models.MMU import MMU
# from Algorithms.FIFO import FIFO
# from Algorithms.MRU import MRU
# from Algorithms.OPT import OPT
# from Algorithms.RND import RND
# from Algorithms.SC import SC
# from interface import MainWindow
# from PyQt5.QtWidgets import QApplication
# import sys
import random

def read_file(file_path):
    operations = []
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            operations.append(line.strip())
            line = file.readline()
    file.close()
    return operations

def run_operations(operations):
    for operation in operations:
        if operation[0] == 'n':
            operation = operation[4:] # remove 'new('
            operation = operation[:-1] # remove ')'
            operation = operation.split(',')

            operation[0] = operation[0].strip()
            operation[1] = operation[1].strip()

            run_new(operation[0], operation[1])

        elif operation[0] == 'u':
            operation = operation[4:] # remove 'use('
            operation = operation[:-1] # remove ')'            
            run_use(operation)

        elif operation[0] == 'd':
            operation = operation[7:] # remove 'delete('
            operation = operation[:-1] # remove ')'
            run_delete(operation)

        elif operation[0] == 'k':
            operation = operation[5:] # remove 'kill('
            operation = operation[:-1] # remove ')'
            run_kill(operation)
        else:
            print('Invalid operation')


def run_new(pid, size):
    print('Running new with pid: ' + pid + ' and size: ' + size)

def run_use(ptr):
    print('Running use with ptr: ' + ptr )

def run_delete(ptr):
    print('Running delete with ptr: ' + ptr)

def run_kill(pid):
    print('Running kill with pid: ' + pid)


def generate_file(seed, operations_amount, process_amount):
    print(seed, operations_amount, process_amount)    
    random.seed(seed) 
    
    with open('operations.txt', 'w') as file:
        ptr_count = []
        process_count = process_amount 
        current_ptrs = []
        deleted_ptrs = []
        to_kill_ptrs = []

        for i in range(process_amount):
            ptr_count.append(i)
        
        choices = ['new', 'use', 'delete']
        probabilities = [0.2, 0.3, 0.1]
        
        while operations_amount != 0:
            if len(deleted_ptrs) == len(ptr_count):
                break
            
            operation = random.choices(choices, weights=probabilities)[0]
              
            if operation == 'new':
                ptr_to_add = random.randint(1, len(ptr_count))
                if ptr_to_add not in deleted_ptrs:
                    file.write(f"new({ptr_to_add}, {random.randint(1, 10000)})\n")
                    if ptr_to_add not in current_ptrs:
                        current_ptrs.append(ptr_to_add)
                    operations_amount -= 1 
                    if ptr_to_add not in to_kill_ptrs:
                        operations_amount -= 1 # save the space for its kill operation
                        to_kill_ptrs.append(ptr_to_add)
            elif operation == 'use':
                ptr_to_use = random.randint(1, len(ptr_count))
                if ptr_to_use in current_ptrs:
                    file.write(f"use({ptr_to_use})\n")
                    operations_amount -= 1
            elif operation == 'delete':
                ptr_to_delete = random.randint(1, len(ptr_count))
                if ptr_to_delete in current_ptrs and ptr_to_delete not in deleted_ptrs:
                    file.write(f"delete({ptr_to_delete})\n")
                    current_ptrs.remove(ptr_to_delete)
                    deleted_ptrs.append(ptr_to_delete)
                    operations_amount -= 1

        for ptr in to_kill_ptrs:
            file.write(f"kill({ptr})\n")

                
    file.close()


# if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()

    # #operations = read_file('test_1.txt')
    # #run_operations(operations)
    # #generate_file(seed=123, operations_amount=20, process_amount=5)


    # sys.exit(app.exec_())

