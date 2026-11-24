
class StableStateDetector:

    def __init__(self, required_frames=5):

        self.required_frames = required_frames

        self.current_candidate = None
        self.stable_state = None

        self.frame_count = 0

    def update(self, new_state):

        # Check whether the new state matches
        # the previous candidate state
        if new_state == self.current_candidate:

            self.frame_count += 1

        else:

            self.current_candidate = new_state
            self.frame_count = 1

        # Accept the state after enough frames
        if self.frame_count >= self.required_frames:

            self.stable_state = self.current_candidate

        return self.stable_state
