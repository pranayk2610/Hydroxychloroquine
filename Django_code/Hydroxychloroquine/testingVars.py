
######### BEGIN SECTION FOR TESTING
# for testing buildings in account.html and reportTest.html
# (both use selectBuildings.html)
class test_Building:
    def __init__(self, name=None,building_id=None):
        self.name=name
        self.building_id=building_id

test_building_names=[
    "Boyd",
    "MLC",
    "Bolton",
    "Chemistry",
    "Ecology",
    "Physics",
    "Plant Sciences",
    "SLC",
    "Creswell",
    "Rutherford",
    "Ramsey",
    "Snelling",
    "Myers",
    "Connor Hall",
    "Tate",
    ]

test_buildings=[test_Building(name) for name in test_building_names]

# for testing the display of reports in home.html
# (both use selectBuildings.html)
class test_report:
    def __init__(self, DateReported=None,Position=None,DateLastOnCampus=None,BuildingsImpacted=None):
        self.DateReported=DateReported
        self.Position=Position
        self.DateLastOnCampus=DateLastOnCampus
        self.BuildingsImpacted=BuildingsImpacted
test_reports=[
    test_report('October 4, 2020','Student','October 2, 2020','Boyd Graduate Research Building, Science Library, Conner Hall, and Miller Learning Center'),
    test_report('October 5, 2020','Student','October 3, 2020','Boyd Graduate Research Building, Science Library, and Miller Learning Center'),
    test_report('October 6, 2020','Student','October 4, 2020','Boyd Graduate Research Building, Science Library, and Miller Learning Center'),
    test_report('October 7, 2020','Student','October 5, 2020','Boyd Graduate Research Building, Science Library, Conner Hall, and Miller Learning Center'),
    test_report('October 8, 2020','Student','October 6, 2020','Boyd Graduate Research Building, Science Library, and Miller Learning Center'),
    test_report('October 9, 2020','Student','October 7, 2020','Boyd Graduate Research Building, Science Library, Conner Hall, and Miller Learning Center'),
    test_report('October 10, 2020','Student','October 8, 2020','Boyd Graduate Research Building, Science Library, and Miller Learning Center'),
    ]
