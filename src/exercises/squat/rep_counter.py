
class SquatCounter:
    def __init__(self):
        self.rep_count = 0
        self.state = "STANDING"
        self.reached_target_depth = False

    def update(self, squat_state, depth_reached=False):

        if self.state == "STANDING":

            if squat_state in ["MOVING", "BOTTOM"]:
                self.state = "GOING_DOWN"
                self.reached_target_depth = depth_reached

        elif self.state == "GOING_DOWN":

            if depth_reached:
                self.reached_target_depth = True

            if squat_state == "BOTTOM":
                self.state = "GOING_UP"

            elif squat_state == "STANDING":
                self.state = "STANDING"
                self.reached_target_depth = False

        elif self.state == "GOING_UP":

            if depth_reached:
                self.reached_target_depth = True

            if squat_state == "STANDING":

                if self.reached_target_depth:
                    self.rep_count += 1

                self.state = "STANDING"
                self.reached_target_depth = False

        return self.rep_count

    def reset_pending_rep(self):
        """Cancel an incomplete repetition without resetting total reps."""

        self.state = "STANDING"
        self.reached_target_depth = False
