from IPython.testing.globalipapp import get_ipython
from IPython.utils.capture import capture_output


class TestSmartPip:
    ip = get_ipython()

    def test_smart_pip(self):
        res = self.ip.run_cell("import smart_pip")
        assert res.success
        self.ip.run_line_magic("pip", "install nothing==0.0.2 -f data")
        self.ip.run_cell("import nothing")
        with capture_output() as captured:
            self.ip.run_line_magic("pip", "install nothing==0.0.3 -f data")
        assert (
            "You should restart Python because the underlying files are updated for these imported modules: nothing"
            in captured.stdout
        )
