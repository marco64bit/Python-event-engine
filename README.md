Python-event-engine
===================

Configurable python event engine to notify a attribute change in your application calling some callback function, inspired to angular

===================
all examples is main.py

a basic example here
<pre>
#how to add a event
def foo(old_val, new_val):
  #do something
  print old_val, new_val
  
scope.first = "test"
scope.add("first", foo)
scope.first = "test change"
</pre>

<pre>
scope.remove("first", foo)
</pre>
