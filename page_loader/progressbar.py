from progress.bar import Bar


class ProgressBar(Bar):
    def finish(self):
        if self.file and self.is_tty() and self.max > 0:
            print(file=self.file)
