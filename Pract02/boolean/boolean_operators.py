#1
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))
#2
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))
#3
x = 200
print(isinstance(x, int))
