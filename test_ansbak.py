from ansbak import main
from textwrap import dedent


def test_main_groups_hosts(capsys):
    ansible_output = dedent("""\
        red01 | CHANGED | rc=0 >>
        foo
        red02 | CHANGED | rc=0 >>
        foo
    """).splitlines()
    main(ansible_output)
    captured = capsys.readouterr()

    expected_output = dedent("""\
        red01,red02 | CHANGED | rc=0 >>
        foo
    """)
    assert captured.out == expected_output
