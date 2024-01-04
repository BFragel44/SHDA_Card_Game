# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:59:09 2022

@author: brett
"""

# GREY = 13 = Each time LC rolls SKULL while ATTACKING, make 1 additional attack.
# GREEN = 3 = Each time a GREEN teammate rolls 4, kill up to THREE from defending swarm.
# RED = 8 = BROTHER LEON can attack up to THREE times.

grey_cards = {
    'attack_card':{
        'ac_name':' Psionic Attack',
        'ac_number':15,
        'ac_effect':'Each time LC\nrolls SKULL while\nATTACKING, make 1\nadditional attack.'},
    'support_card':{
        'ac_name':'Power Field',
        'ac_number':6,
        'ac_effect':'After SUPPORT\nresolved, choose\nany SWARM. They\ncan\'t attack or\nbe killed this\nround.'},
    'move_act_card':{
        'ac_name':'Stealth Tactics',
        'ac_number':8,
        'ac_effect':'After MVE/ACT,\nyou may DISCARD 1\ncard from a blip\npile. Spend 1\nTOKEN to discard\n1 card from other pile.'}}

green_cards = {
    'attack_card':{
        'ac_name':'   Dead Aim',
        'ac_number':16,
        'ac_effect':'each time 1 of\nTEAM rolls 4,\nKILL up to 3\nXenos from the\ndefending swarm.'},
    'support_card':{
        'ac_name':'  Block',
        'ac_number':1,
        'ac_effect':'Each time GIDEON\nrolls a SKULL\nwhile DEFENDING,\nthe attack\nMISSES.'},
    'move_act_card':{
        'ac_name':'  Run and Gun',
        'ac_number':12,
        'ac_effect':'After MVE/ACT\nresolved, each\nof TEAM may\nspend 1 TOKEN\nto make 1 ATTACK'}}

red_cards = {
    'attack_card':{
        'ac_name':'   Full Auto',
        'ac_number':17,
        'ac_effect':'BROTHER LEON may\nATTACK up to 3\ntimes instead of\nonce.'},
    'support_card':{
        'ac_name':'Overwatch',
        'ac_number':4,
        'ac_effect':'At end of the\nEVENT PHASE,\neach TEAM may\nspend 1 TOKEN\nfor 1 ATTACK.'},
    'move_act_card':{
        'ac_name':'Onward Brothers',
        'ac_number':7,
        'ac_effect':'Each time 1 of\nTEAM activates\na DOOR, you may\nplace 1 extra\nTOKEN on the\nTERRAIN'}}

all_sm_action_cards = {3: green_cards, 8: red_cards, 13: grey_cards}