def func():
    print('func is called.')

class A:
    def __init__(self,name='A'):
        self.name=name

    def _say(self,msg):
        print(msg)

    def sayhello(self):
        print('hello,i am {}'.format(self.name))


class B:
    def __init__(self,name='B'):
        self.name=name

    def _do_work(self):
        print('Do some work.')

    def greet(self):
        print('hello,i am {}'.format(self.name))