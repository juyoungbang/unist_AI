# Acknowledgment
This project is a work of UNIST 2020 Spring Artificial Intelligence class. 

# Introduction
Recently, the food delivery market is continuously growing and the number of customers using such service is increasing. Due to such explosive increase, the possible routes of delivering have become complicated and drivers reached the limit of making efficient delivery plans manually. This kind of inefficient path planning leads to drivers' reduce on their own profit and create longer delays for their customers. Based on this point, we would like to propose an efficient delivery route through automated planning which will further expand the delivery market and build a win-win system for all customers, stores and drivers.

# Software Package
In this project, Fast Downward package was used. Fast Downward is a free software package which enables users to run planners. It includes diverse planners such as those that participated in the International Planning Competition(IPC). The planner is mainly developed under Linux and all of its features should work with no restrictions under this platform. The planner should compile and run correctly on macOS, but we cannot guarantee that it works as well as under Linux. The same comment applies for Windows.

# Requirement
The source code of Fast Downward does not have to be manually downloaded since it is already included in this project. Still, the following requirements need to be satisfied for running this project.

- Python >= 3.6
- Mercurial bersion control system
- C++11 compiler
- CMake
- GNU make

# Run
First, you have to build the planner using the following command. It can take up to 20 minutes.
```sh
$ cd downward_package
$ ./build.py
```

Then you can run the planner using the following command. More options can be found at http://www.fast-downward.org/HomePage.
```sh
$ downward_package/fast-downward.py domain.pddl problem1.pddl --search "astar(lmcut())"
```

# Implementation
**Path Generation Section**
When the list of orders come in to the server, it should be in the format given in solver/inputs/problem1.json. This json file will be converted to a PDDL format file by the following code.
```sh
$ base_dir = pathlib.Path().absolute()
$ save_dir = os.path.join(base_dir, 'solver', 'results')
$ import_dir = os.path.join(base_dir, 'solver', 'inputs')

$ with open(os.path.join(import_dir, f'problem{input_num}.json')) as fp:
$     test_data = json.load(fp)['requests']
    
$ builder = ProblemFile(f"problem{input_num}", import_dir, import_dir, test_data)
$ builder.export()
```
The converted file will be in the format given in solver/inputs/problem1.pddl. Then the Fast Downward algorithm will be executed using the script in solver/run_fd.sh. The result file will be generated in solver/results/sas_plan. The sas_plan file can not be used directly, so it is again transformed to the format of our system.The transformed file will be generated in solver/results/plan1.csv.

**User Interface Section**
The generated path information is send to users using Kakaotalk. To enable this, the server has to be started by running main.py.

These three files communicate with the Kakaotalk channel and sends the required responses. The detailed information about Kakaotalk API can be found at https://i.kakao.com/docs/skill-response-format#skillpayload.
- main.py
- scheduling.py
- verification.py

This file includes information about the drivers that are currently registered to our service. The file will refuse the schedule request if the driver is not registered in this file.
- user_info.csv

This directory includes images that are required when sending responses to the Kakaotalk channel.
- etc

This directory includes the source codes of Fast Downward. Note that some of the files of Fast Downward are not pushed to this git due to memory limitation problem.
- downward_package

For making the situation simple in the demo, we made a simple coordinate system of 10*20 to locate stores and customers. However, to show how our service provides the solutions using Kakao Map, we needed some actual locations. To remove this gap, we defined this location mapping file which maps each locations in the original 10*20 coordinate to an actual location. 
- solver/location_mapping.csv

This file reads the planning result and reformats it in a way that the Kakaotalk API can understand.
- solver/data_rapping.py