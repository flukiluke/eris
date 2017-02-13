class Poll:
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options
        self.votes = {}
        for option in options:
            self.votes[option] = []

    def vote(self, user, option):
        if option not in self.options:
            raise LookupError
        for voters in self.votes.values():
            if user in voters:
                voters.remove(user)
        self.votes[option].append(user)

    def results(self):
        return self.votes

    def options_string(self):
        if len(self.options) == 0:
            return "<No options>"
        else:
            return '"' + '", "'.join(self.options[:-2] + ('" or "'.join(self.options[-2:]),)) + '"'
