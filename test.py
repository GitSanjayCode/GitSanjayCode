import string

def string_processing(string_list):
   opstring = ''.join([x for x in ' '.join(string_list) if not x in string.punctuation]).lower()
   return(opstring)

print(string_processing(['test...', 'me....', 'please']))
print(string.punctuation)
  
