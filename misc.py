

import time

def random(num):
    variable = num

    while variable != 4:
        print(f'variable = {variable}')
        print('waiting on resource...')
        time.sleep(3)
        variable += 1

    return variable
        

print(random(0))