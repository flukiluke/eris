class Poll:
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options
        self.votes = {}

    def vote(self, user, option):
        # check option is valid
        self.votes[user] = option

    def results(self):
        results = {}
        results = results.fromkeys(self.options, 0)
        for key in self.votes:
            results[self.votes[key]] += 1
        return results

    def options_string(self):
        if len(self.options) == 0:
            return "<No options>"
        elif len(self.options) < 3:
            return ' or '.join(self.options)
        else:
            return ', '.join(self.options[:-2] + (' or '.join(self.options[-2:]),))

