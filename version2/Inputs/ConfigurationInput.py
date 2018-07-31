# should probably just use java for management / should be JSON not python
#need to run the counts on strains in parallel

def foo(input):
    return input > 1
    
pipes = {
    
    '00_01': {
        'head': {
            'machine': {
                'inventory_group': '',
                },
            'variables': [],
            'functions': {
                
                }
            },
        'body': {
            'directory': '',
            'command': '',
            'type': 'one_to_many',
            'runOnCondition': foo,
            'input': {},
            'output': []
            }
        },
    
    '01_02': {
        'head': {
            'machine': {
                'inventory_group': '',
                },
            'variables': []
            },
        'body': {
            'directory': '',
            'command': '',
            'type': 'parallel',
            'inventory_group': '',
            'input': [],
            'output': [] 
            }
        },
    
    '02_03': {
        'head': {
            'machine': {
                'inventory_group': '',
                },
            'variables': []
            },
        'body': {
            'directory': '',
            'command': '',
            'type': 'join',
            'inventory_group': '',
            'input': [],
            'output': {}
            }
        },
    
    '03_04': {
        'head': {
            'machine': {
                'inventory_group': '',
                },
            'variables': []
            },
        'body': {
            'directory': '',
            'command': '',
            'type': 'linear',
            'input': {},
            'output': {}
            }
        }
    
    }