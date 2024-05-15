# Create Resource objects.
from factryengine import Resource, Scheduler, Task
from datetime import datetime, timezone, timedelta


# Function definitions
def int_to_datetime(num, start_time):
    try:
        # Parse the start time string into a datetime object
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        # Add the number of minutes to the start datetime
        delta = timedelta(minutes=num)
        result_datetime = start_datetime + delta
        return result_datetime

    except Exception:
        print(num)


# CREATE RESOURCE OBJECTS
# We create 5 resources with the same availability.
availability = [(0, 500), (600, 1080), (1200, 1700)]
r1 = Resource(id=1, available_windows=availability)
r2 = Resource(id=2, available_windows=availability)
r3 = Resource(id=3, available_windows=availability)
r4 = Resource(id=4, available_windows=availability)
r5 = Resource(id=5, available_windows=availability)


# CREATE GROUPS OR RESOURCE GROUPS THAT WILL COMBINE RESOURCES TOGETHER
# THIS GROUP WILL BE A LIST OF RESOURCES
group1 = [r1, r2, r3]
group2 = [r4, r5]
group3 = [r1, r2, r5]


# CREATE THE TASKS.
# THE TASKS SHOULD ALREADY BE PREPROCESSED AND ALREADY HAVE AN ASSIGNED LIST OF RESOURCE TO COMPLETE THE TASK
# IN FACTRYFLOW, THE "RESOURCE ASSIGNMENT RULE" WILL DETERMINE WHICH GROUP WILL BE ASSIGNED TO THE TASK

t1 = Task(id=1, duration=300, resources=group1, priority=1, constraints=[r1])
t2 = Task(
    id=2,
    duration=400,
    resources=group2,
    priority=2,
    constraints=[r1],
    predecessors=[t1],
)
t3 = Task(id=3, duration=360, resources=group3, constraints=[r1], priority=4)
t4 = Task(
    id=4,
    duration=100,
    resources=group3,
    priority=3,
    constraints=[r1],
    predecessors=[t1, t3],
)
t5 = Task(id=5, duration=250, resources=group1, constraints=[r1], priority=5)
tasks = [t1, t2, t3, t4, t5]


solution = Scheduler(tasks=tasks, resources=[r1, r2, r3, r4, r5]).schedule()
res_df = solution.to_dataframe()

print(solution.to_dict())

# TO CONVERT INTERVAL INTEGERS TO DATETIME, WE SHOULD HAVE AN OVERALL START TIME
# THAT MARKS AS THE BEGINNING OF THE SCHEDULER -- THIS WILL BE THE 0 TIME
today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
today_str = str(today)[:19]
print("Today: ", today_str)


# WE CONVERT TASK STARTS TO DATE TIME. YOU CAN USE THE FUNCTION ABOVE TO DO THAT.
res_df["planned_task_start"] = res_df.apply(
    lambda x: int_to_datetime(x["task_start"], today_str), axis=1
)
res_df["planned_task_end"] = res_df.apply(
    lambda x: int_to_datetime(x["task_end"], today_str), axis=1
)


# OUTPUT
print(res_df.to_dict(orient="records"))
