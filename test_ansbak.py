from ansbak import main
from textwrap import dedent


def test_main_groups_hosts(capsys):
    ansible_output = dedent("""\
        red01 | CHANGED | rc=0 >>
        foo
        red02 | CHANGED | rc=0 >>
        foo
    """).splitlines(keepends=True)
    main(ansible_output)
    captured = capsys.readouterr()

    expected_output = dedent("""\
        red01,red02 | CHANGED | rc=0 >>
        foo

    """)
    assert captured.out == expected_output


def test_main_groups_hosts_with_different_output(capsys):
    ansible_output = dedent("""\
        red01 | CHANGED | rc=0 >>
        foo
        red02 | CHANGED | rc=0 >>
        bar
        red03 | CHANGED | rc=0 >>
        foo
    """).splitlines(keepends=True)
    main(ansible_output)
    captured = capsys.readouterr()

    expected_output = dedent("""\
        red01,red03 | CHANGED | rc=0 >>
        foo

        --------------------
        red02 | CHANGED | rc=0 >>
        bar

    """)
    assert captured.out == expected_output


def test_main_shows_unreachables_condensed_at_start(capsys):
    ansible_output = dedent("""\
        red01 | CHANGED | rc=0 >>
        foo
        unreachable03 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable03 port 22: No route to host",
            "unreachable": true
        }
        red02 | CHANGED | rc=0 >>
        foo
        unreachable04 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable04 port 22: Operation timed out",
            "unreachable": true
        }
    """).splitlines(keepends=True)
    main(ansible_output)
    captured = capsys.readouterr()

    expected_output = dedent("""\
        unreachable03 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable03 port 22: No route to host",
            "unreachable": true
        }

        unreachable04 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable04 port 22: Operation timed out",
            "unreachable": true
        }

        --------------------
        red01,red02 | CHANGED | rc=0 >>
        foo

    """)
    assert captured.out == expected_output

def test_main_shows_changed_after_failed_after_unreachable(capsys):
    ansible_output = dedent("""\
        red01 | CHANGED | rc=0 >>
        succeeding
        red02 | FAILED | rc=1 >>
        failing
        unreachable03 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable03 port 22: Connection refused",
            "unreachable": true
        }
    """).splitlines(keepends=True)
    main(ansible_output)
    captured = capsys.readouterr()

    expected_output = dedent("""\
        unreachable03 | UNREACHABLE! => {
            "changed": false,
            "msg": "Failed to connect to the host via ssh: ssh: connect to host unreachable03 port 22: Connection refused",
            "unreachable": true
        }

        --------------------
        red02 | FAILED | rc=1 >>
        failing

        --------------------
        red01 | CHANGED | rc=0 >>
        succeeding

    """)
    assert captured.out == expected_output
