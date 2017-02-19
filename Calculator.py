from __future__ import print_function, division
import cmd


class Calculator(cmd.Cmd):
      prompt = 'calc >>> '
      intro = 'Simple calculator that can do addition, subtraction, multiplication and division.'

      def do_add(self, line):
              args = line.split()
              total = 0
              for arg in args:
                      total += float(arg.strip())
              print(total)

      def help_add(self):
              print('\n'.join([
                      'add [number,]',
                      'Add the arguments together and display the total.'
              ]))

      def do_subtract(self, line):
              args = line.split()
              total = 0
              if len(args) > 0:
                      total = float(args[0])
              for arg in args[1:]:
                      total -= float(arg.strip())
              print(total)

      def help_subtract(self):
              print('\n'.join([
                      'subtract [number,]',
                      'Subtract all following arguments from the first argument.'
              ]))

      def do_multiply(self, line):
              args = line.split()
              total = 1
              if len(args) == 0:
                  total = 0
              for arg in args:
                      total *= float(arg.strip())
              print(total)

      def help_multiply(self):
              print('\n'.join([
                      'multiply [number,]',
                      'Multiply the arguments together and display the net results.'
              ]))

      def do_divide(self, line):
              args = line.split()
              if len(args) < 2 or len(args) > 3:
                  print ('Invalid input. Refer help.')
              else:
                disp_remainder = False
                if len(args) == 3 and args[2].lower().strip() == 'true':
                    disp_remainder = True
                numerator = args[0]
                denominator = args[1]
                try:
                    if disp_remainder:
                        print('Quotient: ' + str(float(int(float(numerator)/float(denominator)))) + ', Remainder: ' + str(float(numerator)%float(denominator)))
                    else:
                        print(float(numerator)/float(denominator))
                except:
                    print ('Invalid division')

      def help_divide(self):
              print('\n'.join([
                      'divide [numerator, denominator, display_remainder]',
                      'Divides the numerator by denominator.',
                      'Outputs quotient and remainder if third argument is true.'
              ]))

      def do_EOF(self, line):
              print('bye, bye')
              return True


if __name__ == '__main__':
      Calculator().cmdloop()