from eis.shunting_yard import ShuntingYard


def test_dash():
    shunting_yard = ShuntingYard()
    result = shunting_yard.run_str("A - B")
    assert result == "A B -"


def test_pipe():
    shunting_yard = ShuntingYard()
    result = shunting_yard.run_str("A | B")
    assert result == "A B |"


def test_parenthesis():
    shunting_yard = ShuntingYard()
    result = shunting_yard.run_str("( A - B ) | C")
    assert result == "A B - C |"


def test_parenthesis2():
    shunting_yard = ShuntingYard()
    result = shunting_yard.run_str("A - ( B | C )")
    assert result == "A B C | -"


def test_parenthesis3():
    shunting_yard = ShuntingYard()
    result = shunting_yard.run_str("A - ( B | C - D )")
    assert result == "A B C D - | -"
