from pydspnel.types import *

def assert_lineage(ordered_list):
    for i, t1 in enumerate(ordered_list):
        t1 = types_env[t1]
        for j, t2 in enumerate(ordered_list):
            t2 = types_env[t2]
            ## i < j ==> t1 < t2
            assert (not (i < j)) or (t1 < t2)
            ## i > j ==> t1 > t2
            assert (not (i > j)) or (t1 > t2)

def assert_uncomparable(set_1, set_2):
    for i, t1 in enumerate(set_1):
        t1 = types_env[t1]
        for j, t2 in enumerate(set_2):
            t2 = types_env[t2]
            try:
                t1 < t2
                assert False
            except:
                pass

def test_strict_less_than():
    for t in types_env.values():
        assert t.__lt__(t) == False, repr(t)

def test_self_equals():
    for t in types_env.values():
        assert t == t, repr(t)

def test_lattice():
    assert_lineage(['f32', 'f64', 'float', 'complex', 'number'])

    unsigned_lineage = ['u8', 'u16', 'u32', 'natural', 'integer', 'float', 'complex', 'number']
    assert_lineage(unsigned_lineage)

    signed_lineage = ['i8', 'i16', 'i32', 'integer', 'float', 'complex', 'number']
    assert_lineage(signed_lineage)

    assert_uncomparable(['i8', 'i16', 'i32'], ['u8', 'u16', 'u32', 'natural'])

    stream_unsigned_lineage = ['stream<' + k + '>' for k in unsigned_lineage]
    assert_lineage(stream_unsigned_lineage)

    stream_signed_lineage = ['stream<' + k + '>' for k in signed_lineage]
    assert_lineage(stream_signed_lineage)

def test_arith():
    assert types_env['integer'].add(types_env['integer']) == types_env['integer']
    assert types_env['integer'].add(types_env['float']) == types_env['float']
    
    assert types_env['float'].add(types_env['float']) == types_env['float']

    assert types_env['float'] > (types_env['integer'])
    assert types_env['integer'] < (types_env['float'])
    assert types_env['integer'] != (types_env['float'])
    assert types_env['float'] != (types_env['integer'])


    assert max(types_env['integer'], types_env['float']) == types_env['float']
    assert max(types_env['float'], types_env['integer']) == types_env['float']
    assert types_env['float'].add(types_env['integer']) == types_env['float']