# Create Resource objects.
from factryengine import Resource, Scheduler, Task, Assignment, ResourceGroup
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
r1 = Resource(id=1, available_windows=[(540, 720), (10620, 10800), (20700, 20880), (30780, 30960), (40860, 41040)])
r2 = Resource(id=2, available_windows=[(3480, 3960), (13560, 14040), (23640, 24120), (33720, 34200), (43800, 44280)])
r3 = Resource(id=3, available_windows=[(4980, 5460), (15060, 15540), (25140, 25620), (35220, 35700), (45300, 45780)])
r4 = Resource(id=4, available_windows=[(3480, 3960), (13560, 14040), (23640, 24120), (33720, 34200), (43800, 44280)])
r5 = Resource(id=5, available_windows=[(3480, 3960), (13560, 14040), (23640, 24120), (33720, 34200), (43800, 44280)])


# CREATE GROUPS OR RESOURCE GROUPS THAT WILL COMBINE RESOURCES TOGETHER
# THIS GROUP WILL BE A LIST OF RESOURCES
group1 = ResourceGroup(resources=[r1, r2, r3])
group2 = ResourceGroup(resources=[r4, r5])
group3 = ResourceGroup(resources=[r1, r2, r5])


# CREATE THE TASKS.
# THE TASKS SHOULD ALREADY BE PREPROCESSED AND ALREADY HAVE AN ASSIGNED LIST OF RESOURCE TO COMPLETE THE TASK
# IN FACTRYFLOW, THE "RESOURCE ASSIGNMENT RULE" WILL DETERMINE WHICH GROUP WILL BE ASSIGNED TO THE TASK

assignment_task_1 = Assignment(resource_groups=[group2], resource_count=1)

t1 = Task(id=1, duration=300, resources=group1, priority=1, constraints=[r1], assignment=[assignment_task_1])
t2 = Task(
    id=2,
    duration=400,
    resources=group2,
    priority=2,
    constraints=[r3],
    predecessors=[t1],
)
t3 = Task(id=3, duration=360, resources=group3, constraints=[r2], priority=4)
t4 = Task(
    id=4,
    duration=100,
    resources=group3,
    priority=3,
    constraints=[r1],
    predecessors=[t1, t3],
)
t5 = Task(id=5, duration=250, resources=group1, constraints=[r3], priority=5)
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

print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

# OUTPUT
print(res_df.to_dict(orient="records"))
