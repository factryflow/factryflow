from job_manager.models.task import Task

from microbatching.models.microbatch_flow import (
    MicrobatchFlow,
    MicrobatchTask,
    MicrobatchTaskFlow,
)


def gather_flow_branches(start_task, flow=None):
    """Recursively gather flow branches starting from a given start task.
    Multiple branches are created for one flow if a Task in the flow
    has multiple predecessors.
    """
    if flow is None:
        flow = []

    # Add the current task to the flow
    flow.append(start_task)

    # Get successors of the current tas
    successors = start_task.get_successors()

    if not successors.exists():
        # If there are no successors, return the current flow as a branch
        return [flow]

    # Collect all branches
    branches = []
    for successor in successors:
        # Recursive call to gather branches from the successor
        branches.extend(gather_flow_branches(successor, flow.copy()))

    return branches


def list_microbatch_task_flows(start_rule, min_flow_length=2, max_flow_length=3):
    """List all TaskFlows for a MicrobatchFlow using the MicrobatchFlow start_rule."""

    # Get all starting_tasks
    starting_tasks = Task.objects.filter(
        microbatchruletaskmatch__microbatch_rule=start_rule
    )

    task_flow_list = []

    for task in starting_tasks:
        # Gather flows starting from this starting_task
        flows = gather_flow_branches(start_task=task)
        if flows:
            for branch in flows:
                if (
                    len(branch) >= min_flow_length and len(branch) <= max_flow_length
                ):  # Only include flows that meet the length requirements
                    task_flow_list.append(branch)

    return task_flow_list


def create_task_flows():
    """Create MicrobatchTaskFlows for all MicrobatchFlows."""
    result = {}
    try:
        # Clear MicrobatchTaskFlows and MicrobatchTasks
        MicrobatchTaskFlow.objects.all().delete()
        MicrobatchTask.objects.all().delete()

        flow_count = 0

        # Run list_microbatch_task_flows for all MicrobatchFlows
        for microbatch_flow in MicrobatchFlow.objects.all():
            task_flow_list = []
            generated_flows = list_microbatch_task_flows(
                start_rule=microbatch_flow.start_rule,
                min_flow_length=microbatch_flow.min_flow_length,
                max_flow_length=microbatch_flow.max_flow_length,
            )

            task_flow_list.extend(generated_flows)
            flow_count += len(generated_flows)

            if task_flow_list:  # Create MicrobatchTaskFlows
                for task_list in task_flow_list:
                    task_flow = MicrobatchTaskFlow.objects.create(
                        microbatch_flow=microbatch_flow
                    )
                    order_index = 0

                    for task in task_list:
                        MicrobatchTask.objects.create(
                            task=task,
                            microbatch_task_flow=task_flow,
                            order=order_index,
                        )
                        order_index += 1

        if flow_count:
            result["message"] = f"Generated {flow_count} TaskFlows."
        else:
            result["message"] = "No Tasks matched with any MicrobatchFlow"
        result["status"] = "success"

        return result

    except Exception as e:
        result["message"] = str(e)
        result["status"] = "error"
        return result
