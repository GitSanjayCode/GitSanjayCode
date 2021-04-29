set serveroutput on ;
declare
type rec is record
(empno number,
 ename varchar2(100));
type rec_typ is table of rec;
rec_t rec_typ;
cursor c1 is 
select empno,ename 
from emp;
begin
  dbms_output.put_line('Sanjay Start ');
  open c1;
   loop
    fetch c1 bulk collect into rec_t limit 5;
    dbms_output.put_line('rec count '||rec_t.count);
    dbms_output.put_line('before update');
    for i in 1 .. rec_t.count loop
      dbms_output.put_line('emp '||rec_t(i).empno||' '||'ename '||rec_t(i).ename);
    end loop;
    
    forall i in 1 .. rec_t.count
     update emp e set e.comm=2 where e.EMPNO=rec_t(i).empno and e.ENAME=rec_t(i).ename;
     
     dbms_output.put_line('After update');
    for i in 1 .. rec_t.count loop
      dbms_output.put_line('emp '||rec_t(i).empno||' '||'ename '||rec_t(i).ename);
    end loop;
    exit when rec_t.count=0;
   end loop;
  close c1;
  
  dbms_output.put_line('rec count '||rec_t.count);
  
  
  
end;