# -*- coding: utf-8 -*-
"""
test_repeat.py
"""
from pyxform.tests_v1.pyxform_test_case import PyxformTestCase


class TestRepeat(PyxformTestCase):
    """
    TestRepeat class.
    """
    def test_repeat_relative_reference(self):
        """
        Test relative reference in repeats.
        """
        self.assertPyxformXform(
            name="test_repeat",
            title="Relative Paths in repeats",
            md="""
                | survey |              |          |            |                      |
                |        | type         | name     | relevant   | label                |
                |        | text         | Z        |            | Fruit                |
                |        | begin repeat | section  |            | Section              |
                |        | text         | AA       |            | Anything really      |
                |        | text         | A        |            | A oat                |
                |        | text         | B        | ${A}='oat' | B w ${A}             |
                |        | note         | note1    |            | Noted ${AA} w ${A}   |
                |        | end repeat   |          |            |                      |
                |        |              |          |            |                      |
                |        | begin repeat | section2 |            | Section 2            |
                |        | text         | C        |            | C                    |
                |        | begin group  | sectiona |            | Section A            |
                |        | text         | D        |            | D oat                |
                |        | text         | E        | ${D}='oat' | E w ${Z}             |
                |        | note         | note2    |            | Noted ${C} w ${E}    |
                |        | end group    |          |            |                      |
                |        | note         | note3    |            | Noted ${C} w ${E}    |
                |        | end repeat   |          |            |                      |
                |        |              |          |            |                      |
                |        | begin repeat | section3 |            | Section 3            |
                |        | text         | FF       |            | F any text           |
                |        | text         | F        |            | F oat                |
                |        | begin group  | sectionb |            | Section B            |
                |        | text         | G        |            | G oat                |
                |        | text         | H        | ${G}='oat' | H w ${Z}             |
                |        | note         | note4    |            | Noted ${H} w ${Z}    |
                |        | end group    |          |            |                      |
                |        | begin repeat | sectionc |            | Section B            |
                |        | text         | I        |            | I                    |
                |        | text         | J        | ${I}='oat' | J w ${Z}             |
                |        | text         | K        | ${F}='oat' | K w ${Z}             |
                |        | text         | L        | ${G}='oat' | K w ${Z}             |
                |        | note         | note5    |            | Noted ${FF} w ${H}   |
                |        | note         | note6    |            | JKL #${J}#${K}#${L}  |
                |        | end repeat   |          |            |                      |
                |        | note         | note7    |            | Noted ${FF} w ${H}   |
                |        | begin group  | sectiond |            | Section D            |
                |        | text         | M        |            | M oat                |
                |        | text         | N        | ${G}='oat' | N w ${Z}             |
                |        | text         | O        | ${M}='oat' | O w ${Z}             |
                |        | note         | note8    |            | NO #${N} #${O}       |
                |        | end group    |          |            |                      |
                |        | note         | note9    |            | ${FF} ${H} ${N} ${N} |
                |        | end repeat   |          |            |                      |
                |        |              |          |            |                      |
                """,
            instance__contains=[
                '<section jr:template="">',
                '<A/>',
                '<B/>',
                '</section>',
                ],
            model__contains=[
                """<bind nodeset="/test_repeat/section/A" """
                """type="string"/>""",
                """<bind nodeset="/test_repeat/section/B" """
                """relevant=" current()/../A ='oat'" """
                """type="string"/>""",
                """<bind nodeset="/test_repeat/section2/sectiona/E" """
                """relevant=" current()/../D ='oat'" type="string"/>""",
                """<bind nodeset="/test_repeat/section3/sectionc/K" """
                """relevant=" current()/../../F ='oat'" type="string"/>""",
                """<bind nodeset="/test_repeat/section3/sectionc/L" """
                """relevant=" current()/../../sectionb/G ='oat'" """
                """type="string"/>""",
                """<bind nodeset="/test_repeat/section3/sectiond/N" """
                """relevant=" current()/../../sectionb/G ='oat'" """
                """type="string"/>"""
                ],
            xml__contains=[
                '<group ref="/test_repeat/section">',
                '<label>Section</label>',
                '</group>',
                """<label> B w <output value=" current()/../A "/> </label>""",
                """<label> E w <output value=" /test_repeat/Z "/> </label>""",
                """<label> Noted <output value=" current()/../FF "/> w """
                """<output value=" current()/../sectionb/H "/> </label></input>"""
            ],
            run_odk_validate=True
        )

    def test_calculate_relative_path(self):
        """Test relative paths in calculate column."""
        self.assertPyxformXform(
            name="data",
            title="Choice filter uses relative path",
            md="""
                | survey  |                      |       |        |                |
                |         | type                 | name  | label  | calculate      |
                |         | begin repeat         | rep   |        |                |
                |         | select_one crop_list | crop  | Select |                |
                |         | text                 | a     | Verify | name = ${crop} |
                |         | begin group          | group |        |                |
                |         | text                 | b     | Verify | name = ${crop} |
                |         | end group            |       |        |                |
                |         | end repeat           |       |        |                |
                |         |                      |       |        |                |
                | choices |                      |       |        |                |
                |         | list name            | name  | label  |                |
                |         | crop_list            | maize | Maize  |                |
                |         | crop_list            | beans | Beans  |                |
                |         | crop_list            | kale  | Kale   |                |
            """,
            model__contains=[
                """<bind calculate="name =  current()/../crop " """
                """nodeset="/data/rep/a" type="string"/>""",
                """<bind calculate="name =  current()/../../crop " """
                """nodeset="/data/rep/group/b" type="string"/>""",
            ]
        )
