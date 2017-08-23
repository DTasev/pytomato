import sys


class SoundBoard():
    def __init__(self, mute):
        self.mute = mute

    def play_notification_sound(self):
        if not self.mute and sys.platform == 'win32':
            import winsound
            return winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
        else:
            def play_notification_sound(self):
                # simply do nothing as we don't know how to play sound on the platform we're on
                pass
