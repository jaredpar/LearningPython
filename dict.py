
class Foo(object):
    ham = 42

f = Foo()
print 'f has ham: {0}'.format(hasattr(f, 'ham'))
print 'f has bar: {0}'.format(hasattr(f, 'bar'))

# Class attributes are available via the instances

Foo.bar = 42
print 'f has bar: {0}'.format(hasattr(f, 'bar'))
