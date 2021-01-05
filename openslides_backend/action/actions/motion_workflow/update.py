from ....models.models import MotionWorkflow
from ...generics.update import UpdateAction
from ...util.default_schema import DefaultSchema
from ...util.register import register_action


@register_action("motion_workflow.update")
class MotionWorkflowUpdateAction(UpdateAction):
    """
    Action to update a motion workflow.
    """

    model = MotionWorkflow()
    schema = DefaultSchema(MotionWorkflow()).get_update_schema(
        optional_properties=["name", "first_state_id"]
    )
    permission_description = "motion.can_manage"