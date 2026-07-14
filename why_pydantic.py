# we have to write manual code we have to perform type validation and data validation and 
# we would have to do in every function making code compex and violate dry principle of programming

def insert(name:str,age:int):
    if type(name)==str and type(age)==int:
        if age>0:
            print(name)
            print(age)
            print('inserted into file')
        else:
            raise ValueError('not negative')
    else:
        raise TypeError('type mismatch')
    

insert('musa',20)
# now same for update function it works but is not scalable!!!
# for exmaple if db had 10 fields type validatio  and data validation on all 10 fields
# and in many functions makes the code messy and complex

