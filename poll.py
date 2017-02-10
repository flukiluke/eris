class Poll:
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options
        self.votes = dict.fromkeys(options)

    def vote(self, user, option):
        if option not in self.options:
            raise LookupError
        if self.votes[option] is None:
            self.votes[option] = [user]
        else:
            self.votes[option].append(user)

    def results(self):
        return self.votes

    def options_string(self):
        if len(self.options) == 0:
            return "<No options>"
        else:
            return '"' + '", "'.join(self.options[:-2] + ('" or "'.join(self.options[-2:]),)) + '"'
