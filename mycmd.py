from __future__ import print_function, division
import cmd


class mycmd(cmd.Cmd):
      prompt = 'mycmd $ '
      intro = 'Test for command line interpreter with deploy, kill, benchmark and report.'

      def do_deploy(self, line):

              print('deploy')

      def help_deploy(self):
              print('\n'.join([
                      'deploy [args,]',
                      'Some explainaiton.'
              ]))
      def do_benchmark(self, line):

              print('benchmark')

      def help_benchmark(self):
              print('\n'.join([
                      'benchmark [args,]',
                      'Some explainaiton.'
              ]))
      def do_report(self, line):

              print('report')

      def help_report(self):
              print('\n'.join([
                      'report [args,]',
                      'Some explainaiton.'
              ]))
      def do_kill(self, line):

              print('kill')

      def help_kill(self):
              print('\n'.join([
                      'kill [args,]',
                      'Some explainaiton.'
              ]))

      def do_EOF(self, line):
          print('exiting mycmd')
          return True

if __name__ == '__main__':
    mycmd().cmdloop()