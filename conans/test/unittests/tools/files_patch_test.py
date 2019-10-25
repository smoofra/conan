    test_profile
        self.assertIn("patch_ng: error: no patch data found!", client.out)
    def test_add_new_file(self):
        """ Validate issue #5320
        """

        conanfile = dedent("""
            from conans import ConanFile, tools
            import os
            
            class ConanFileToolsTest(ConanFile):
                name = "foobar"
                version = "0.1.0"
                exports_sources = "*"
            
                def build(self):
                    tools.patch(patch_file="add_files.patch")
                    assert os.path.isfile("foo.txt")
                    assert os.path.isfile("bar.txt")
        """)
        bar = "no creo en brujas"
        patch = dedent("""
            From c66347c66991b6e617d107b505c18b3115624b8a Mon Sep 17 00:00:00 2001
            From: Uilian Ries <uilianries@gmail.com>
            Date: Wed, 16 Oct 2019 14:31:34 -0300
            Subject: [PATCH] add foo
            
            ---
             bar.txt | 3 ++-
             foo.txt | 3 +++
             2 files changed, 5 insertions(+), 1 deletion(-)
             create mode 100644 foo.txt
            
            diff --git a/bar.txt b/bar.txt
            index 0f4ff3a..0bd3158 100644
            --- a/bar.txt
            +++ b/bar.txt
            @@ -1 +1,2 @@
            -no creo en brujas
            +Yo no creo en brujas, pero que las hay, las hay
            +
            diff --git a/foo.txt b/foo.txt
            new file mode 100644
            index 0000000..91e8c0d
            --- /dev/null
            +++ b/foo.txt
            @@ -0,0 +1,3 @@
            +For us, there is no spring.
            +Just the wind that smells fresh before the storm.
            +
            -- 
            2.23.0


        """)

        client = TestClient()
        client.save({"conanfile.py": conanfile,
                     "add_files.patch": patch,
                     "bar.txt": bar})
        client.run("install .")
        client.run("build .")
        bar_content = load(os.path.join(client.current_folder, "bar.txt"))
        self.assertIn(dedent("""Yo no creo en brujas, pero que las hay, las hay
                             """), bar_content)
        foo_content = load(os.path.join(client.current_folder, "foo.txt"))
        self.assertIn(dedent("""For us, there is no spring.
Just the wind that smells fresh before the storm."""), foo_content)
        self.assertIn("Running build()", client.out)
        self.assertNotIn("Warning", client.out)

        ret = loader.load_consumer(file_path, test_profile())