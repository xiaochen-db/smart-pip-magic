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

    def test_smart_pip_when_orignal_pip_nonexistent(self):
        self.ip.run_cell("import smart_pip")
        self.ip.run_line_magic("pip", "install nothing==0.0.2 -f data")
        self.ip.run_cell("import nothing")
        with capture_output() as captured:
            self.ip.run_line_magic("pip", "install nothing==0.0.3 -f data")
        assert (
            "You should restart Python because the underlying files are updated for these imported modules: nothing"
            in captured.stdout
        )

    def test_smart_pip_with_module_reload_hook(self):
        self.ip.run_cell("""
                        import smart_pip
                        def h(s):
                            print('hook called on ' + str(s))
                        smart_pip.add_reload_hook(h)
                         """)
        self.ip.run_line_magic("pip", "install nothing==0.0.2 -f data")
        self.ip.run_cell("import nothing")
        with capture_output() as captured:
            self.ip.run_line_magic("pip", "install nothing==0.0.3 -f data")
        assert (
            "You should restart Python because the underlying files are updated for these imported modules: nothing"
            in captured.stdout
        )
        assert "hook called on ['nothing']" in captured.stdout

    def test_smart_pip_with_all_hooks_cleare(self):
        self.ip.run_cell("""
                        import smart_pip
                        def h(s):
                            print('hook called on ' + str(s))
                        smart_pip.add_reload_hook(h)
                         """)
        self.ip.run_cell("smart_pip.clear_all_hooks()")
        self.ip.run_line_magic("pip", "install nothing==0.0.2 -f data")
        self.ip.run_cell("import nothing")
        with capture_output() as captured:
            self.ip.run_line_magic("pip", "install nothing==0.0.3 -f data")
        assert "hook called on ['nothing']" not in captured.stdout
