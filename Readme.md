Pre-Requisites -> Python3 , Ubuntu OS (Recommended)

# Setup

1. clone the files from the git cloud location ```git@git.aconex.cloud:hackathon/october-2017/intellispect.git```

2. Install morse simulator from ```https://www.openrobots.org/morse/doc/stable/user/installation.html```

3. install all pip3 packages ```pip3 install -r requirements.txt```

note: python3-tk to be installed separately based on operating system

# Execution

1. Run morse simulator by giving a command

     ```morse run intellispect.py```
     
2. Run the drone simulation using the following command

     ```python3 scripts/flight_controller.py```

note: the drone simulation will be in manual mode.

# Navigation Instructions

The following keys can be used for navigation

left -> Move left

right -> Move right

up -> move forward

down -> move backward

a -> turn left

d -> turn right

w -> move up

s -> move down   