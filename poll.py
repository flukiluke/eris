class Poll:
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options
        self.votes = []

    def vote(self, user, option):
        # check option is valid
        self.votes[user] = option

    def results(self):
        results = []
        results.fromkeys(options, 0)
        for key in self.votes:
            results[votes[key]] += 1
        return results

