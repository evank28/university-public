# Note: Code is modified to prevent
from io import StringIO
from group_hierarchy import *
import pytest
from copy import deepcopy


# ======================== TO-DO ITEMS ========================

# ======================== Helper Functions ========================

def __eq__employee(e1: Member, e2: Member) -> bool:
    """
    Compares two employees, recursively comparing subordinates for equality, if needed.
    """
    eid_eq = e1.eid == e2.eid
    name_eq = e1.name == e2.name
    position_eq = e1.position == e2.position
    wage_eq = e1.wage == e2.wage
    rating_eq = e1.rating == e2.rating
    # if e1._superior is not None or e1._superior is not None:
    #     sup_eq = __eq__employee(e1._superior, e2._superior)
    # else:
    #     sup_eq = True
    length = len(e1._subordinates)
    sub_eq = length == len(e2._subordinates)
    if sub_eq and length > 0:
        for i in range(length):
            if not __eq__employee(e1._subordinates[i], e2._subordinates[i]):
                return False
    return eid_eq and name_eq and position_eq and wage_eq and rating_eq # and sup_eq


# ======================== Generic Tests ========================


def test_no_sorted_methods() -> None:
    file = open('group_hierarchy.py', 'r').read()
    found = file.count('.sort(') + file.count('sorted(')
    # Note that the starter code included these words in comments 4 times
    assert found <= 4, "Per instructions, 'You must NOT use list.sort() or sorted() in your code.'" \
                       " These functions were used {} times.".format(found - 4)


# Test merge
def test_t1_merge_empty() -> None:
    l1 = []
    l2 = []
    assert merge(l1, l2) == []


def test_t1_merge_singlesame() -> None:
    l1 = [1]
    l2 = [1]
    assert merge(l1, l2) == [1, 1]


def test_t1_merge_singlediff() -> None:
    l1 = [2]
    l2 = [1]
    assert merge(l1, l2) == [1, 2]


def test_t1_merge_mix() -> None:
    l1 = [5, 12, 3, 8, 2]
    l2 = [2, 1, 15, 4]
    assert merge(sorted(l1), sorted(l2)) == [1, 2, 2, 3, 4, 5, 8, 12, 15]


# Test create_organization_from_file
def test_t6_create_organization_from_file_sample() -> None:
    o = create_organization_from_file(open('employees.txt'))
    assert isinstance(o, grouping)
    assert isinstance(o._head, Leader), "failed to recognize head as a leader"
    assert o._head.name == 'Alice'
    assert o._head.position == 'CEO'
    assert o._head.wage == 250000
    assert o._head.rating == 20
    assert o._head._department_name == "Some Corp."
    e2 = o.get_employee(2)
    assert e2.name == 'Dave' and e2.position == 'CFO' and e2.wage == 150000 and e2.rating == 30 \
        and e2._department_name == 'Finance' and isinstance(e2, Leader) and e2.get_superior().eid == 1
    e8 = o.get_employee(8)
    assert e8.name == 'Carol' and e8.position == 'Secretary' and e8.wage == 60000 and e8.rating == 40 \
        and e8.get_department_name() == 'Some Corp.' and not isinstance(e8, Leader) and e8.get_superior().eid == 1
    e9 = o.get_employee(9)
    assert e9.name == 'Fred' and e9.position == 'Hiring Manager' and e9.wage == 60000 and e9.rating == 10 \
        and e9.get_department_name() == 'Human Resources' and not isinstance(e9, Leader) and \
        e9.get_superior().eid == 5 and e9.get_all_subordinates() == []
    e13 = o.get_employee(13)
    assert e13.name == 'Kevin' and e13.position == 'Programmer' and e13.wage == 40000 and e13.rating == 80 \
        and e13.get_department_name() == 'Technology' and not isinstance(e13, Leader) and \
        e13.get_superior().eid == 12 and o.get_employee(12).get_superior().eid == 10 and \
        e13.get_all_subordinates() == []
    e11 = o.get_employee(11)
    assert e11.name == 'Joe' and e11.position == 'Programmer' and e11.wage == 60000 and e11.rating == 90 \
        and e11.get_department_name() == 'Technology' and not isinstance(e11, Leader) and \
        e11.get_superior().eid == 12 and o.get_employee(12).get_superior().eid == 10 and \
        o.get_employee(10).get_superior().eid == 1 and e11.get_all_subordinates()[0].eid == 15


def test_t6_create_organization_from_file_empty() -> None:
    FILE = StringIO('')
    o = create_organization_from_file(FILE)
    assert isinstance(o, grouping)
    assert o._head is None


def test_t6_create_organization_from_file_one_employee() -> None:
    FILE = '25,Fred,Chef du Rien,50,1'
    o = create_organization_from_file(StringIO(FILE))
    assert isinstance(o, grouping)
    assert isinstance(o._head, Member) and not isinstance(o._head, Leader)
    assert o._head.eid == 25 and  o._head.name == "Fred" and  o._head.position == "Chef du Rien" and \
        o._head.wage == 50 and o._head.rating == 1
    assert o._head.get_superior() is None and o._head.get_all_subordinates() == []


def test_t6_create_organization_from_file_one_leader() -> None:
    FILE = '25,Fred,Chef du Rien,50,1,,La Crotte Corporation'
    o = create_organization_from_file(StringIO(FILE))
    assert isinstance(o, grouping)
    assert isinstance(o._head, Leader)
    assert o._head.eid == 25 and o._head.name == "Fred" and  o._head.position == "Chef du Rien" and \
        o._head.wage == 50 and o._head.rating == 1
    assert o._head.get_superior() is None and o._head.get_all_subordinates() == []


def test_t6_create_organization_from_file_mutlilevel_departments() -> None:
    """ This method tests for an organization with multiple levels of department"""
    # Please, if you read the following file, appreciate the intricacy of the plot (draw it out) :) ;) :O
    FILE = """
    1,Bill,President,200000,60,,White House\n
    2,Hillary,Secretary of State,100000,5,1,State Dept\n
    10,Monica Lewinsky,Secretary,60000,100,1\n
    5,Priv ate Server,IT Head,80000,40,2,IT Dept\n
    7,Ben Ghazi,Guard,30000,1,2\n
    20,Gho Stpen,Communications Chair,50000,70,10,Communications Dept\n
    9,Codey Mon Key,Private Server Supervisor,20000,95,5\n
    30,Sandy Smith,Comms Intern,15000,75,20
    """
    o = create_organization_from_file(StringIO(FILE))
    assert isinstance(o, grouping)
    e1 = o.get_employee(1)
    assert e1.name == 'Bill' and e1.position == 'President' and e1.wage == 200000 and e1.rating == 60 \
        and e1.get_department_name() == 'White House' and isinstance(e1, Leader) and e1.get_superior() is None
    e2 = o.get_employee(2)
    assert e2.name == 'Hillary' and e2.position == 'Secretary of State' and e2.wage == 100000 and e2.rating == 5 \
        and e2.get_department_name() == 'State Dept' and isinstance(e2, Leader) and e2.get_superior().eid == 1
    e10 = o.get_employee(10)
    assert e10.name == 'Monica Lewinsky' and e10.position == 'Secretary' and \
           e10.wage == 60000\
        and e10.rating == 100 and e10.get_department_name() == 'White House' and not isinstance(e10, Leader) \
        and e10.get_superior().eid == 1
    e5 = o.get_employee(5)
    assert e5.name == 'Priv ate Server' and e5.position == 'IT Head' and e5.wage == 80000 and e5.rating == 40 \
        and e5.get_department_name() == 'IT Dept' and isinstance(e5, Leader) and e5.get_superior().eid == 2
    e7 = o.get_employee(7)
    assert e7.name == 'Ben Ghazi' and e7.position == 'Guard' and e7.wage == 30000 \
        and e7.rating == 1 and e7.get_department_name() == 'State Dept' and not isinstance(e7, Leader) \
        and e7.get_superior().eid == 2
    e20 = o.get_employee(20)
    assert e20.name == 'Gho Stpen' and e20.position == 'Communications Chair' and e20.wage == 50000 and \
        e20.rating == 70 and e20.get_department_name() == 'Communications Dept' and isinstance(e20, Leader) and \
        e20.get_superior().eid == 10
    e9 = o.get_employee(9)
    assert e9.name == 'Codey Mon Key' and e9.position == 'Private Server Supervisor' and e9.wage == 20000 \
        and e9.rating == 95 and e9.get_department_name() == 'IT Dept' and not isinstance(e9, Leader) \
        and e9.get_superior().eid == 5
    e30 = o.get_employee(30)
    assert e30.name == 'Sandy Smith' and e30.position == 'Comms Intern' and \
           e30.wage == 15000 \
        and e30.rating == 75 and e30.get_department_name() == 'Communications Dept' and not isinstance(e30, Leader) \
        and e30.get_superior().eid == 20 and e30.get_superior().get_superior().get_superior().eid == 1


def test_t1___init__1() -> None:
    x = Member(1, 'emp1', 'Director', 15.00, 1)
    assert x.eid == 1
    assert x.name == 'emp1'
    assert x.position == 'Director'
    assert x.wage == 15.00
    assert x.rating == 1
    assert isinstance(x, Member)
    assert isinstance(x._subordinates, list)


def test_t1___init__2() -> None:
    x = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    assert x.eid == 20
    assert x.name == "Bob The Builder"
    assert x.position == 'Construction Member'
    assert x.wage == 8.00
    assert x.rating == 100
    assert isinstance(x, Member)
    assert isinstance(x._subordinates, list)


#  Test __lt__
def test_t1___lt__lt() -> None:
    x1 = Member(1, 'emp1', 'Director', 15.00, 1)
    x2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    assert x1 < x2


def test_t1___lt__eq() -> None:
    x1 = Member(1, 'emp1', 'Director', 15.00, 1)
    x2 = Member(1, 'emp1', 'Director', 15.00, 1)
    ret = x1.__lt__(x2)
    assert ret is not None
    assert not ret


def test_t1___lt__gt() -> None:
    x1 = Member(1, 'emp1', 'Director', 15.00, 1)
    x2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    ret = x2.__lt__(x1)
    assert ret is not None
    assert not ret


# Test get_direct_subordinates and get_all_subordinates and get_organization_head
def test_t1_subordinates_and_head_simple() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)

    # Make e1 > e2
    e2._superior = e1
    e1._subordinates = [e2]
    # Make e2 > e3
    e3._superior = e2
    e2._subordinates = [e3]
    assert e1.get_direct_subordinates() == [e2]
    assert e2.get_direct_subordinates() == [e3]
    assert e1.get_all_subordinates() == [e2, e3], "get_all_subordinates fails in a chain -- also check sort order"
    assert e2.get_all_subordinates() == [e3]
    assert e3.get_direct_subordinates() == [], "Fails when there are no subordinates"
    assert e3.get_all_subordinates() == [], "Fails when there are no subordinates"
    assert e3.get_organization_head() == e1
    assert e2.get_organization_head() == e1
    assert e1.get_organization_head() == e1, "fails when called on the head"


# Test get_direct_subordinates and get_all_subordinates and get_employee and get_employees_paid_more_than
def test_t1_subordinates_and_head_and_get_and_paidmorethan__large() -> None:
    # depends on a working become_subordinate method
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    e9 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e5 = Member(50, "Fa the Doorman", 'Hospitality Member', 32.00, 100)
    e6 = Member(60, "George the Doorman", 'Hospitality Member', 8.00, 100)
    e7 = Member(70, "Hugh the Heighty", 'Big Boss', 12.00, 100)
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7
       e4       e9     e1
     e8  e2             e5
                       e6 e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # Row 1 - check
    assert e7.get_direct_subordinates() == [e9, e4, e1]
    assert e7.get_all_subordinates() == [e8, e9, e3, e4, e5, e6, e1, e2]
    # Row 2 -- Check
    assert e4.get_direct_subordinates() == [e8, e2]
    assert e4.get_all_subordinates() == [e8, e2]
    assert e9.get_direct_subordinates() == []
    assert e9.get_all_subordinates() == []
    assert e1.get_direct_subordinates() == [e5]
    assert e1.get_all_subordinates() == [e3, e5, e6]
    # Row 3 - Check
    assert e8.get_direct_subordinates() == []
    assert e8.get_all_subordinates() == []
    assert e2.get_direct_subordinates() == []
    assert e2.get_all_subordinates() == []
    assert e5.get_direct_subordinates() == [e3, e6]
    assert e5.get_all_subordinates() == [e3, e6]
    # Row 4 - Check
    assert e6.get_direct_subordinates() == []
    assert e6.get_all_subordinates() == []
    assert e3.get_direct_subordinates() == []
    assert e3.get_all_subordinates() == []
    # Check Head -- simplified
    assert e3.get_organization_head() == e7
    assert e2.get_organization_head() == e7
    assert e9.get_organization_head() == e7
    assert e5.get_organization_head() == e7
    assert e7.get_organization_head() == e7, "fails when called on the head"
    # Check get_employee
    assert e7.get_employee(90) == e2, "fails for target on same row"
    assert e8.get_employee(40) is None, "fails for target 1 row above"
    assert e8.get_employee(70) is None, "fails for target 2 rows above"
    assert e8.get_employee(1) == e8, "fails for target that is self"
    assert e7.get_employee(50) == e5, "fails for target in lateral subtree"
    assert e8.get_employee(30) is None, "fails for target in lateral subtree and below"
    assert e7.get_employee(1) == e8, "fails for target 2 rows below"
    assert e5.get_employee(30) == e3, "fails for target directly below"
    assert e7.get_employee(100) is None, "fails when target not in organization"
    # Check get_employees_paid_more_than
    assert e7.get_employees_paid_more_than(15.00) == [e3, e4, e5, e2], "failed implementation -- note that e8 does not" \
                                                                       "qualify since 15.00 is NOT < 15.00"
    assert e7.get_employees_paid_more_than(7.99) == [e8, e9, e3, e4, e5, e6, e7, e1, e2]
    assert e7.get_employees_paid_more_than(32.00) == []
    assert e8.get_employees_paid_more_than(7.99) == [e8]
    assert e8.get_employees_paid_more_than(15.00) == []
    assert e1.get_employees_paid_more_than(19.00) == [e3, e5]


# Test get_superior
def test_t1_get_superior_none() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    assert e1.get_superior() is None, "Your function fails when <self> has no superior"


def test_t1_get_superior_chain() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)

    # manual changes, in case become_subordinate does not work
    # Make e1 > e2
    e2._superior = e1
    e1._subordinates = [e2]
    # Make e2 > e3
    e3._superior = e2
    e2._subordinates = [e3]
    assert e2.get_superior() == e1, "get_superior is not implemented properly"
    assert e3.get_superior() == e2, "get_superior is not implemented properly"


def test_t1_get_superior_multichain() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)

    # manual changes, in case become_subordinate does not work
    # Make e1 > e2
    e2._superior = e1
    e1._subordinates = [e2, e3]
    # Make e2 > e3
    e3._superior = e1
    assert e2.get_superior() == e1, "get_superior is not implemented properly"
    assert e3.get_superior() == e1, "get_superior is not implemented properly"


# Test become_subordinate
def test_t1_become_subordinate() -> None:
    # assumes that __init__, get_superior, and get_direct_subordinates work correctly
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e2_copy = deepcopy(e2)
    e2.become_subordinate(e1)
    assert id(e2.get_superior()) == id(e1), "Your function improperly assigns the superior"
    assert __eq__employee(e2.get_superior(), e1), "Your function improperly assigns the superior"
    assert __eq__employee(e2_copy, e2), "Your function improperly mutates superior"
    assert id(e1.get_direct_subordinates()[0]) == id(e2), "Your function failed to mutate the superior's " \
                                                          "_subordinates attribute"


def test_t1_become_subordinate_switch() -> None:
    # assumes that __init__, get_superior, and get_direct_subordinates work correctly
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)
    e2.become_subordinate(e1)
    assert id(e2.get_superior()) == id(e1), "Your function improperly assigns the superior"
    assert __eq__employee(e2.get_superior(), e1), "Your function improperly assigns the superior"
    assert id(e1.get_direct_subordinates()[0]) == id(e2), "Your function failed to mutate the superior's " \
                                                          "_subordinates attribute"
    e2.become_subordinate(e3)
    assert id(e2.get_superior()) == id(e3), "Your function improperly assigns the superior when a change of superiority" \
                                        " is made"
    assert e1.get_direct_subordinates() == [], "You failed to modify the original superior's _subordinates attribute " \
                                               "for a case when someone gets re-assigned from under them"


# Test remove_subordinate_id
def test_t1_remove_subordinate_id_only() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)
    e2.become_subordinate(e1)
    e3.become_subordinate(e2)
    e2.remove_subordinate_id(30)
    assert e2.get_all_subordinates() == []
    assert e2.get_direct_subordinates() == []
    assert e1.get_all_subordinates() == [e2]
    assert e1.get_direct_subordinates() == [e2]
    assert e3._superior == e2, "You should NOT change the employee with eid <eid>'s superior"


def test_t1_remove_subordinate_id_position() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 16.00, 100)
    e5 = Member(50, "Fa the Doorman", 'Hospitality Member', 16.00, 100)
    e6 = Member(60, "George the Doorman", 'Hospitality Member', 16.00, 100)
    e7 = Member(70, "Hugh the Heighty", 'Big Boss', 16.00, 100)
    e1._subordinates = [e3, e2, e4, e5, e6, e7]
    e1.remove_subordinate_id(30)
    assert e1._subordinates == [e2, e4, e5, e6, e7], "removal from front failed"
    e1.remove_subordinate_id(70)
    assert e1._subordinates == [e2, e4, e5, e6], "removal from end failed"
    e1.remove_subordinate_id(50)
    assert e1._subordinates == [e2, e4, e6], "removal from middle failed"


# Test add_subordinate
def test_t1_add_subordinate() -> None:
    # assumes correctly working get_direct_subordinates
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    e2 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 16.00, 100)
    e1.add_subordinate(e2)
    assert e1.get_direct_subordinates() == [e2], "bad implementation"
    e1.add_subordinate(e3)
    assert e1.get_direct_subordinates() == [e2, e3], "does not work when >=1 subordinate to <self> already exists"


# Test get_employees_paid_more_than -- more above!
def test_t1_get_employees_paid_more_than_just_one() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 1)
    assert e1.get_employees_paid_more_than(14.00) == [e1]
    assert e1.get_employees_paid_more_than(15.00) == []
    assert e1.get_employees_paid_more_than(16.00) == []


# TODO: Compile correct list of Task 1 functions from client_code and write appropriate tests


# ======================== Task 2 Tests ========================

# Test get_department_name and get_position_in_hierarchy
def test_t2_get_department_name_and_position_none() -> None:
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    assert e8.get_department_name() == '', "fails when the employee is not part of a department"
    assert e8.get_position_in_hierarchy() == 'Director'


def test_t2_get_department_name__and_position_large() -> None:
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    e9 = Leader(20, "Bob The Builder", 'Construction Member', 8.00, 100, "HR")
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e5 = Leader(50, "Fa the Doorman", 'Hospitality Member', 32.00, 100, "Facilities")
    e6 = Leader(60, "George the Toilet Cleaner", 'Hospitality Member', 8.00, 100, "Sanitation")
    e7 = Leader(70, "Hugh the Heighty", 'Big Boss', 12.00, 100, "AlphaHotel")
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7 (AlphaHotel)
       e4       e9(HR)     e1
     e8  e2                  e5 (Facilities)
                     e6(Sanitation) e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # Testing get_department_name
    assert e7.get_department_name() == 'AlphaHotel'
    assert e4.get_department_name() == 'AlphaHotel'
    assert e2.get_department_name() == 'AlphaHotel'
    assert e9.get_department_name() == 'HR'
    assert e1.get_department_name() == 'AlphaHotel'
    assert e5.get_department_name() == 'Facilities'
    assert e6.get_department_name() == 'Sanitation'
    assert e3.get_department_name() == 'Facilities'
    # Testing get_position_in_hierarchy
    assert e7.get_position_in_hierarchy() == 'Big Boss, AlphaHotel'
    assert e4.get_position_in_hierarchy() == 'Hospitality Member, AlphaHotel'
    assert e5.get_position_in_hierarchy() == 'Hospitality Member, Facilities, AlphaHotel'
    assert e3.get_position_in_hierarchy() == 'Hospitality Member, Facilities, AlphaHotel'
    assert e6.get_position_in_hierarchy() == 'Hospitality Member, Sanitation, Facilities, AlphaHotel', "all " \
                                                                                                         "sub" \
                                                                                                         "departments" \
                                                                                                         " must be " \
                                                                                                         "included. " \
                                                                                                         "See Piazza " \
                                                                                                         "@898."
    assert e9.get_position_in_hierarchy() == 'Construction Member, HR, AlphaHotel'
    assert e2.get_position_in_hierarchy() == 'Hospitality Member, AlphaHotel'


# TODO: Compile correct list of Task 2 functions from client_code and write appropriate tests

# ======================== Task 3 Tests ========================


# Test get_department_leader
def test_t3_get_department_leader() -> None:
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    e9 = Leader(20, "Bob The Builder", 'Construction Member', 8.00, 100, "HR")
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e5 = Leader(50, "Fa the Doorman", 'Hospitality Member', 32.00, 100, "Facilities")
    e6 = Leader(60, "George the Toilet Cleaner", 'Hospitality Member', 8.00, 100, "Sanitation")
    e7 = Leader(70, "Hugh the Heighty", 'Big Boss', 12.00, 100, "AlphaHotel")
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    e10 = Member(95, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7 (AlphaHotel)
       e4       e9(HR)     e1
     e8  e2                  e5 (Facilities)
                     e6(Sanitation) e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # Check - get_department_leader
    assert e8.get_department_leader() == e7
    assert e10.get_department_leader() is None, "Fails when employee is not in a dept"
    assert e7.get_department_leader() == e7
    assert e9.get_department_leader() == e9, "Fails for sub-department head"
    assert e3.get_department_leader() == e5
    assert e6.get_department_leader() == e6
    assert e1.get_department_leader() == e7


# TODO: Compile correct list of Task 3 functions from client_code and write appropriate tests

# ======================== Task 4 Tests ========================
def test_t4_doctest() -> None:
    e1 = Member(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    new_e1 = e1.swap_up()
    assert isinstance(new_e1, Leader)
    new_e2 = new_e1.get_direct_subordinates()[0]
    assert isinstance(new_e2, Member)
    assert new_e1.position == 'Manager'
    assert new_e1.eid == 1
    assert e3.get_direct_subordinates()[0] is new_e1


# Test get_highest_rated_subordinate and swap_up
def test_t4_get_highest_rated_subordinate_and_swap_up() -> None:
    # NOTE - IF TESTS FAIL HERE, SEE PIAZZA @918 follow up. There is some flexibility for how this is
    # supposed to operate.
    e8 = Member(1, 'emp1', 'Director', 15.00, 40)
    e9 = Leader(20, "Bob The Builder", 'Construction Member', 8.00, 30, "HR")
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 60)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 50)
    e5 = Leader(50, "Fa the Doorman", 'Dept Head', 32.00, 100, "Facilities")
    e6 = Leader(60, "George the Toilet Cleaner", 'Hospitality Member', 8.00, 20, "Sanitation")
    e7 = Leader(70, "Hugh the Heighty", 'Big Boss', 12.00, 100, "AlphaHotel")
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 80)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 15)
    """
    Intended Tree:
            e7 (AlphaHotel)
       e4       e9(HR)     e1
     e8  e2                  e5 (Facilities)
                     e6(Sanitation) e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # Check - get_highest_rated_subordinate
    assert e4.get_highest_rated_subordinate() == e8
    assert e5.get_highest_rated_subordinate() == e3
    assert e1.get_highest_rated_subordinate() == e5
    # Check - swap_up
    e3 = e3.swap_up()
    e5 = e7.get_employee(50)
    assert isinstance(e3, Leader), "Bad Implementation: Class should now be leader"
    assert isinstance(e5, Member), "Bad Implementation: Class should be " \
                                                                    "swapped to Member"
    assert e3.rating == 60 and e5.rating == 100, "Bad Implementation: Do not swap ratings per Piazza @824"
    assert e3.wage == 32.00 and e5.wage == 24.00, "Bad Implementation: You should be swapping salaries"
    assert e3.position == 'Dept Head' and e5.position == 'Hospitality Member', "Bad Implementation: You should be " \
                                                                                 "swapping positions"
    assert e3.get_all_subordinates() == [e5, e6] and e5._subordinates == [], "Bad Implementation: You should be " \
                                                                             "swapping subordinates."
    assert e3._superior == e1 and e5._superior == e3 and e6._superior == e3, "Bad Implementation: Improperly " \
                                                                             "re-assigned superiors."
    """
       New Tree:
               e7 (AlphaHotel)
          e4       e9(HR)     e1
        e8  e2                  e3 (Facilities)
                        e6(Sanitation) e5
       """
    # Next swap_up -- e9
    e9 = e9.swap_up()
    e7 = e9.get_employee(70)
    assert isinstance(e9, Leader) and isinstance(e7, Leader), "Bad Implementation: Both classes should still" \
                                                                        " be leader."
    assert e9.rating == 30 and e7.rating == 100, "Bad Implementation: Do not swap ratings per Piazza @824"
    assert e9.wage == 12.00 and e7.wage == 8.00, "Bad Implementation: You should be swapping salaries"
    assert e9.position == 'Big Boss' and e7.position == 'Construction Member', "Bad Implementation: You should be " \
                                                                                 "swapping positions"
    assert e9.get_all_subordinates() == [e8, e3, e4, e5, e6, e7, e1, e2] and \
           e9.get_direct_subordinates() == [e4, e7, e1] and \
           e7.get_all_subordinates() == [], "Bad Implementation: You should be swapping subordinates."
    assert e7._superior == e9 and e4._superior == e9 and e1._superior == e9 and e9._superior is None, \
        "Bad Implementation: Improperly re-assigned superiors."
    """
          New Tree:
                  e9 (AlphaHotel)
             e4       e7(HR)     e1
           e8  e2                  e3 (Facilities)
                           e6(Sanitation) e5
          """
    # Next swap_up -- e3
    e3 = e3.swap_up()
    e1 = e9.get_employee(80)
    assert isinstance(e3, Member) and isinstance(e1, Leader), "Bad Implementation: Class should be swapped " \
                                                                          "too."
    assert e3.rating == 60 and e1.rating == 80, "Bad Implementation: Do not swap ratings per Piazza @824"
    assert e3.wage == 9.00 and e1.wage == 32.00, "Bad Implementation: You should be swapping salaries"
    assert e3.position == 'Hospitality Member' and e1.position == 'Dept Head', "Bad Implementation: You should be " \
                                                                                 "swapping positions"
    assert e3.get_all_subordinates() == [e5, e6, e1] and e3.get_direct_subordinates() == [e1] and \
           e1.get_all_subordinates() == [e5, e6], "Bad Implementation: You should be swapping subordinates."
    assert e3._superior == e9 and e1._superior == e3 and e6._superior == e1 and e5._superior == e1, \
        "Bad Implementation: Improperly re-assigned superiors."
    """
             New Tree:
                     e9 (AlphaHotel)
                e4       e7(HR)     e3
              e8  e2                  e1 (Facilities)
                              e6(Sanitation) e5
             """
    # Next swap_up -- e8
    e8 = e8.swap_up()
    e4 = e9.get_employee(40)
    assert isinstance(e8, Member) and isinstance(e4, Member), "Bad Implementation: Class should not " \
                                                                            "change."
    assert e8.rating == 40 and e4.rating == 50, "Bad Implementation: Do not swap ratings per Piazza @824"
    assert e8.wage == 20.00 and e4.wage == 15.00, "Bad Implementation: You should be swapping salaries"
    assert e8.position == 'Hospitality Member' and e4.position == 'Director', "Bad Implementation: You should be " \
                                                                                "swapping positions"
    assert e8.get_all_subordinates() == [e4, e2] and \
           e4.get_all_subordinates() == [], "Bad Implementation: You should be swapping subordinates."
    assert e4._superior == e8 and e2._superior == e8 and e8._superior == e9 and e7._superior == e9, \
        "Bad Implementation: Improperly re-assigned superiors."
    """
                New Tree:
                        e9 (AlphaHotel)
                   e8      e7(HR)     e3
                 e4  e2                  e1 (Facilities)
                                 e6(Sanitation) e5
                """


# TODO: Compile correct list of Task 4 functions from client_code and write appropriate tests

# ==============================================================================
# ======================== TESTS FOR grouping CLASS ========================
# ==============================================================================
# Test grouping __init__
def test_t1_org___init__() -> None:
    e1 = Member(1, 'emp1', 'Director', 15.00, 40)
    # empyy
    o1 = grouping()
    assert o1._head is None, 'fails on None case (empty init argument)'
    o2 = grouping(e1)
    assert o2._head == e1
    e2 = Leader(20, "Bob The Builder", 'Construction Member', 8.00, 30, "HR")
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 60)
    o3 = grouping(e2)
    assert o3._head == e2 and isinstance(o3._head, Leader), "fails for a Leader as head"
    e3.become_subordinate(e2)
    o4 = grouping(e3)
    assert o4._head == e3, "fails when the head already had a superior"


# Test grouping get_employee and get_average_wage
def test_t1_org_get_employee_and_average_wage() -> None:
    # depends on get_employee of Member being correct, as tested above
    e8 = Member(1, 'emp1', 'Construction Member', 15.00, 1)
    e9 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e5 = Member(50, "Fa the Doorman", 'Hospitality Member', 32.00, 100)
    e6 = Member(60, "George the Doorman", 'Hospitality Member', 8.00, 100)
    e7 = Member(70, "Hugh the Heighty", 'Big Boss', 12.00, 100)
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7
       e4       e9     e1
     e8  e2             e5
                       e6 e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # grouping Setup
    o = grouping(e7)
    # Tests for get_employee
    id_lst = [1,20,30,40,50,60,70,80,90,100]
    for eid in id_lst:
        assert e7.get_employee(eid) == o.get_employee(eid), f"fails when searching for eid {eid}"
    # Tests for get_average_wage -- these tests are not exhaustive
    assert round(o.get_average_wage(), 4) == round(158/9, 4), "fails when None position is specified"
    assert o.get_average_wage('Software Dev') == 0.0, "fails when <position> not in organization"
    assert round(o.get_average_wage('Hospitality Member'), 4) == round(123 / 6, 4)
    assert round(o.get_average_wage('Construction Member'), 4) == round(23 / 2, 4)
    assert o.get_average_wage('Big Boss') == 12.00, "fails when just 1 employee of that position is present"


# Test grouping add_employee
def test_t1_org_add_employee_and_t5() -> None:
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    e9 = Member(20, "Bob The Builder", 'Construction Member', 8.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e7 = Member(70, "Hugh the Heighty", 'Big Boss', 12.00, 100)
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7
       e4       e9     e1
     e8  e2             
    """
    o = grouping()
    o.add_employee(e4)
    assert o._head == e4, "fails when ID was not specified and head exists already"
    o.add_employee(e7)
    assert o._head == e7, "fails when ID was not specified and head exists already"
    assert o._head._subordinates == [e4], "fails when ID was not specified and head exists already"
    assert e4._superior == e7, "fails when ID was not specified and head exists already"
    o.add_employee(e8, 40)
    assert e4._subordinates == [e8]
    assert e8._superior == e4
    o.add_employee(e9, 70)
    o.add_employee(e1, 70)
    assert e7.get_direct_subordinates() == [e9, e4, e1]
    o.add_employee(e2, 40)
    assert e2.get_direct_subordinates() == []
    assert e2.get_superior() == e4
    # Tests for Task 5
    assert create_department_wage_tree(o) is None, "fails when there are no Leader objects in the org"

# TODO: Compile Tasks 1-4 additional methods for grouping from client code and write tests here

# ==============================================================================
# ======================== TESTS FOR Leader CLASS ==============================
# ==============================================================================

# Test leader __init__


def test_t2_leader___init__() -> None:
    x = Leader(1, 'emp1', 'Director', 15.00, 1, 'IT Department')
    assert x.eid == 1
    assert x.name == 'emp1'
    assert x.position == 'Director'
    assert x.wage == 15.00
    assert x.rating == 1
    assert x._department_name == 'IT Department'
    assert isinstance(x, Member)
    assert isinstance(x._subordinates, list)


# TODO: Compile Tasks 2-4 additional methods for leader from client code and write tests here

# ==============================================================================
# ======================== TESTS FOR DepartmentWageTree CLASS ================
# ==============================================================================

#  Test DepartmentWageTree create_department_wage_tree
def test_t5_dwt_create_department_wage_tree_large() -> None:
    e8 = Member(1, 'emp1', 'Director', 15.00, 1)
    e9 = Leader(20, "Bob The Builder", 'Construction Member', 8.00, 100, "HR")
    e3 = Member(30, "Don the Doorman", 'Hospitality Member', 24.00, 100)
    e4 = Member(40, "Earnest the Doorman", 'Hospitality Member', 20.00, 100)
    e5 = Leader(50, "Fa the Doorman", 'Hospitality Member', 32.00, 100, "Facilities")
    e6 = Leader(60, "George the Toilet Cleaner", 'Hospitality Member', 8.00, 100, "Sanitation")
    e7 = Leader(70, "Hugh the Heighty", 'Big Boss', 12.00, 100, "AlphaHotel")
    e1 = Member(80, "Ian the Doorman", 'Hospitality Member', 9.00, 100)
    e2 = Member(90, "James the Doorman", 'Hospitality Member', 30.00, 100)
    """
    Intended Tree:
            e7 (AlphaHotel)
       e4       e9(HR)     e1
     e8  e2                  e5 (Facilities)
                     e6(Sanitation) e3
    """
    # Row 2 - setup
    e4.become_subordinate(e7)
    e9.become_subordinate(e7)
    e1.become_subordinate(e7)
    # Row 3 - setup
    e8.become_subordinate(e4)
    e2.become_subordinate(e4)
    e5.become_subordinate(e1)
    # Row 4 - setup
    e6.become_subordinate(e5)
    e3.become_subordinate(e5)
    # Setup org
    o = grouping()
    o.add_employee(e7)
    e7_copy = deepcopy(e7)
    # Check DST
    dwt = create_department_wage_tree(o)
    assert isinstance(dwt, DepartmentWageTree)
    assert dwt.department_name == 'AlphaHotel'
    assert round(dwt.wage, 4) == round((12 + 20 + 15 + 30 + 9)/5, 4)
    assert dwt.subdepartments[0].department_name == 'HR'
    assert dwt.subdepartments[0].wage == 8.00
    assert dwt.subdepartments[0].subdepartments == []
    assert len(dwt.subdepartments) == 2, "too many departments included in subdepartments"
    assert dwt.subdepartments[1].department_name == 'Facilities'
    assert round(dwt.subdepartments[1].wage, 4) == round((32 + 24)/2, 4)
    assert len(dwt.subdepartments[1].subdepartments) == 1
    assert dwt.subdepartments[1].subdepartments[0].department_name == 'Sanitation'
    assert dwt.subdepartments[1].subdepartments[0].wage == 8.00
    assert dwt.subdepartments[1].subdepartments[0].subdepartments == []
    # Check that grouping has not been mutated
    assert __eq__employee(o._head, e7_copy)


def test_t5_dwt_create_department_wage_tree_one() -> None:
    e1 = Leader(60, "George the Toilet Cleaner", 'Chef Nottoyeur', 8.00, 100, "Sanitation Corp")
    o = grouping()
    o.add_employee(e1)
    dwt = create_department_wage_tree(o)
    assert isinstance(dwt, DepartmentWageTree)
    assert dwt.department_name == 'Sanitation Corp'
    assert dwt.wage == 8.00
    assert dwt.subdepartments == []


if __name__ == "__main__":
    pytest.main(['test_group_hierarchy.py'])
