
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMMENT DIVIDE LPAREN MINUS NUMBER PLUS RPAREN TIMESexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expressionexpression : LPAREN expression RPARENexpression : NUMBER'
    
_lr_action_items = {'LPAREN':([0,2,4,5,6,7,],[2,2,2,2,2,2,]),'NUMBER':([0,2,4,5,6,7,],[3,3,3,3,3,3,]),'$end':([1,3,9,10,11,12,13,],[0,-6,-1,-2,-3,-4,-5,]),'PLUS':([1,3,8,9,10,11,12,13,],[4,-6,4,4,4,4,4,-5,]),'MINUS':([1,3,8,9,10,11,12,13,],[5,-6,5,5,5,5,5,-5,]),'TIMES':([1,3,8,9,10,11,12,13,],[6,-6,6,6,6,6,6,-5,]),'DIVIDE':([1,3,8,9,10,11,12,13,],[7,-6,7,7,7,7,7,-5,]),'RPAREN':([3,8,9,10,11,12,13,],[-6,13,-1,-2,-3,-4,-5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,4,5,6,7,],[1,8,9,10,11,12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','calcAST.py',8),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','calcAST.py',9),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','calcAST.py',10),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','calcAST.py',11),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','calcAST.py',16),
  ('expression -> NUMBER','expression',1,'p_expression_number','calcAST.py',20),
]