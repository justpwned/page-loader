from progress.bar import Bar


class ProgressBar(Bar):
    def finish(self):
        if self.file and self.is_tty():
            end = '\n' if self.max else ''
            print(file=self.file, end=end)
