# Graph Theory project
# Sammar Tahir

# Represents a state two arrows, labelled by label
# Use None for a label representing "e" arrows
from typing import Any

def shunt(infix):
    """"This function is the Shunting Yard Algorithm for converting
        infix regular expressions to postfix."""
    # Special characters for regular expressions and their precednce
    specials = {'*': 50, '.': 40, '|': 30}

    # Will eventually be the output
    profix = ""
    # Operator stack.
    stack = ""

    # Loop through the string a character at a time
    for c in infix:
        # If an open bracket, push to the stack
        if c == '(':
            stack = stack + c
        # If a closing bracket, pop from stack, push to output until open bracket
        elif c == ')':
            while stack[-1] != '(':
                profix, stack = profix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # If it's an operator, push to stack after popping lower or equal precedence
        # operators from top of stack into output
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                profix, stack = profix + stack[-1], stack[:-1]
            stack = stack + c
        # Regular characters are pushed immediately to the output
        else:
            profix = profix + c

    # Pop all remaining operators from stack to output
    while stack:
        profix, stack = profix + stack[:-1], stack[:-1]

    # Returning postfix regex
    return profix




class state:
     label = None
     edge1 = None
     edge2 = None

#An NFA is represented by its initial and accept states
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def compile(profix):
    """This function complies a postfix regular expression into an NFA."""
    nfaStack = []

    for c in profix:
        if c == '.':
            # Pop two NFA's off the stack
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            # Connect first NFA's accept state tp the second'd initial
            nfa1.accept.edge1 = nfa2.initial
            # Push NFA to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfaStack.append(newnfa)

        elif c == '|':
            # Pop two NFA's off the stack
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            # Create a new initial state, connect it the initial states
            # of the two NFA's popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # Create a new accept state, connecting the accept states
            # of the two NFA's popped from the stack, to the new state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)

        elif c == '*':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)
        else:
            # Create new initial and accept states
            accept = state()
            initial = state()
            # Join the initial state the accept state using an arrow labelled
            initial.label = c
            initial.edge1 = accept
            # Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)

    # nfaStack should only have a single nfa on it at this point
    return nfaStack.pop()

def followes(state):
    """Return the set of states that can be reached from state following e arrows."""

    # Create a new set, with state as its only memeber
    states = set()
    states.add(state)

    # Check if state has arrows labelled e from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it
            states |= followes(state.edge1)
        # Check if edge2 is state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followes(state.edge2)

    #Return the set of state
    return states

def  match(infix, string):
    """Matches string to infix regular expression"""

   # Shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

   # The current set of states and the next set of states
    current = set()
    next = set()

   # Add the initisl state ti the current set
    current |= followes(nfa.initial)

    # Loop through each charatere in the string
    for s in string:
        # Loop through the current set of states
        for c in current:
            # Check if thst state is labelled s
            if c.label == s:
                # Add the edge1 state to the next set
                next |= followes(c.edge1)
        # Set current to next, and clear out next
        current = next
        next = set()

    # Check if the accept state is in the set of current states
    return (nfa.accept in current)

# A few Tests
infixes = ["a.b.c", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b).c"]
string =  ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in  infixes:
    for s in  string: 
        print(match(i, s), i, s)
