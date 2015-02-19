class ChannelMismatchError(Exception):
    def __init__(self, expected, actual):
        message = "Expected {} channels and received {}"
        super(ChannelMismatchError, self).__init__(
            message.format(expected, actual)
        )
