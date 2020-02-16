import pytest
import osd
import nec_tables as nec

sizes = ['12', '10', '8', '6', '4', '3', '2', '1',
         '1/0', '2/0', '3/0', '4/0',
         '250', '300', '350',
         '400', '500', '600', '700',
         '750', '800', '900', '1000',
         '1250', '1500', '1750', '2000']

three_ten_17 = nec.cable_ampacity_310_17

class TestLookup:
    """Tests of lookup function against various NEC tables."""

    def test_warn_lookup_out_of_table(self):
        """Raise warning if the lookup value is outside of the table."""
        with pytest.warns(UserWarning):
            osd.lookup(43, nec.ccc_count_derate)
        with pytest.warns(UserWarning):
            osd.lookup(800, nec.cable_ampacity_310_16['Cu'][90], keys=False)

    def test_ccc_derate_table(self):
        """Test current carrying conductor derate table."""
        assert osd.lookup(3, nec.ccc_count_derate) == 1.0
        assert osd.lookup(2, nec.ccc_count_derate) == 1.0
        assert osd.lookup(4, nec.ccc_count_derate) == 0.8
        assert osd.lookup(5, nec.ccc_count_derate) == 0.8
        assert osd.lookup(10, nec.ccc_count_derate) == 0.5

    def test_cable_ampacities(self):
        """Test lookups against ampacities in Table 310.16."""
        assert osd.lookup(135, nec.cable_ampacity_310_16['Cu'][90],
                          keys=False) == '1'
        assert osd.lookup(225, nec.cable_ampacity_310_16['Cu'][90],
                          keys=False) == '3/0'
        assert osd.lookup(25, nec.cable_ampacity_310_16['Cu'][90],
                          keys=False) == '12'


class TestGetWireSize:
    """Tests of wire size other than lookup values."""

    def test_derate(self):
        """Test the derate functionality."""
        assert osd.get_wire_ampacity('1/0', 'Cu', 90, derates=0.8) == 136

    def test_derate_current_comparison(self):
        """Test the comparison against a passed current."""
        assert osd.get_wire_ampacity('1/0', 'Cu', 90, current=169.9999) is True
        assert osd.get_wire_ampacity('1/0', 'Cu', 90, current=170) is True
        assert osd.get_wire_ampacity('1/0', 'Cu', 90, current=170.001) is False

    def test_derate_and_current_comparison(self):
        """Test the derate and current comparison."""
        assert osd.get_wire_ampacity('1/0', 'Cu', 90, current=153.01,
                                     derates=0.9) is False


class TestGetWireSize310_16:
    """Tests of the get wire ampacity function.

    Expected values from test looked up directly from 2017 NEC not from the
    nec_tables.py file. Serves to also test values in nec_tables.py.
    """

    ampacities_cu_60 = [20, 30, 40, 55, 70, 85, 95, 110,
                        125, 145, 165, 195,
                        215, 240, 260,
                        280, 320, 350, 385,
                        400, 410, 435, 455,
                        495, 525, 545, 555]

    amp_tests_310_16_cu_60 = [(size, 'Cu', 60, exp) for size, exp in
                              zip(sizes, ampacities_cu_60)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_cu_60)
    def test_310_16_cu_60(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected

    ampacities_cu_75 = [25, 35, 50, 65, 85, 100, 115, 130,
                        150, 175, 200, 230,
                        255, 285, 310,
                        335, 380, 420, 460,
                        475, 490, 520, 545,
                        590, 625, 650, 665]

    amp_tests_310_16_cu_75 = [(size, 'Cu', 75, exp) for size, exp in
                              zip(sizes, ampacities_cu_75)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_cu_75)
    def test_310_16_cu_75(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected

    ampacities_cu_90 = [30, 40, 55, 75, 95, 115, 130, 145,
                        170, 195, 225, 260,
                        290, 320, 350,
                        380, 430, 475, 520,
                        535, 555, 585, 615,
                        665, 705, 735, 750]

    amp_tests_310_16_cu_90 = [(size, 'Cu', 90, exp) for size, exp in
                              zip(sizes, ampacities_cu_90)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_cu_90)
    def test_310_16_cu_90(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected

    ampacities_al_60 = [15, 25, 35, 40, 55, 65, 75, 85,
                        100, 115, 130, 150,
                        170, 195, 210,
                        225, 260, 285, 315,
                        320, 330, 355, 375,
                        405, 435, 455, 470]

    amp_tests_310_16_al_60 = [(size, 'Al', 60, exp) for size, exp in
                              zip(sizes, ampacities_al_60)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_al_60)
    def test_310_16_al_60(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected

    ampacities_al_75 = [20, 30, 40, 50, 65, 75, 90, 100,
                        120, 135, 155, 180,
                        205, 230, 250,
                        270, 310, 340, 375,
                        385, 395, 425, 445,
                        485, 520, 545, 560]

    amp_tests_310_16_al_75 = [(size, 'Al', 75, exp) for size, exp in
                              zip(sizes, ampacities_al_75)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_al_75)
    def test_310_16_al_75(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected

    ampacities_al_90 = [25, 35, 45, 55, 75, 85, 100, 115,
                        135, 150, 175, 205,
                        230, 260, 280,
                        305, 350, 385, 425,
                        435, 445, 480, 500,
                        545, 585, 615, 630]

    amp_tests_310_16_al_90 = [(size, 'Al', 90, exp) for size, exp in
                              zip(sizes, ampacities_al_90)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_16_al_90)
    def test_310_16_al_90(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp) == expected


class TestGetWireSize310_17:
    """Tests of the get wire ampacity function.

    Expected values from test looked up directly from 2017 NEC not from the
    nec_tables.py file. Serves to also test values in nec_tables.py.
    """

    ampacities_cu_60 = [30, 40, 60, 80, 105, 120, 140, 165,
                        195, 225, 260, 300,
                        340, 375, 420,
                        455, 515, 575, 630,
                        655, 680, 730, 780,
                        890, 980, 1070, 1155]

    amp_tests_310_17_cu_60 = [(size, 'Cu', 60, exp) for size, exp in
                              zip(sizes, ampacities_cu_60)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_cu_60)
    def test_310_17_cu_60(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected

    ampacities_cu_75 = [35, 50, 70, 95, 125, 145, 170, 195,
                        230, 265, 310, 360,
                        405, 445, 505,
                        545, 620, 690, 755,
                        785, 815, 870, 935,
                        1065, 1175, 1280, 1385]

    amp_tests_310_17_cu_75 = [(size, 'Cu', 75, exp) for size, exp in
                              zip(sizes, ampacities_cu_75)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_cu_75)
    def test_310_17_cu_75(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected

    ampacities_cu_90 = [40, 55, 80, 105, 140, 165, 190, 220,
                        260, 300, 350, 405,
                        455, 500, 570,
                        615, 700, 780, 850,
                        885, 920, 980, 1055,
                        1200, 1325, 1445, 1560]

    amp_tests_310_17_cu_90 = [(size, 'Cu', 90, exp) for size, exp in
                              zip(sizes, ampacities_cu_90)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_cu_90)
    def test_310_17_cu_90(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected

    ampacities_al_60 = [25, 35, 45, 60, 80, 95, 110, 130,
                        150, 175, 200, 235,
                        265, 290, 330,
                        355, 405, 455, 500,
                        515, 535, 580, 625,
                        710, 795, 875, 960]

    amp_tests_310_17_al_60 = [(size, 'Al', 60, exp) for size, exp in
                              zip(sizes, ampacities_al_60)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_al_60)
    def test_310_17_al_60(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected

    ampacities_al_75 = [30, 40, 55, 75, 100, 115, 135, 155,
                        180, 210, 240, 280,
                        315, 350, 395,
                        425, 485, 545, 595,
                        620, 645, 700, 750,
                        855, 950, 1050, 1150]

    amp_tests_310_17_al_75 = [(size, 'Al', 75, exp) for size, exp in
                              zip(sizes, ampacities_al_75)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_al_75)
    def test_310_17_al_75(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected

    ampacities_al_90 = [35, 45, 60, 85, 115, 130, 150, 175,
                        205, 235, 270, 315,
                        355, 395, 445,
                        480, 545, 615, 670,
                        700, 725, 790, 845,
                        965, 1070, 1185, 1295]

    amp_tests_310_17_al_90 = [(size, 'Al', 90, exp) for size, exp in
                              zip(sizes, ampacities_al_90)]

    @pytest.mark.parametrize("size,metal,temp,expected",
                             amp_tests_310_17_al_90)
    def test_310_17_al_90(self, size, metal, temp, expected):
        """Test a wire sizes with defaults."""
        assert osd.get_wire_ampacity(size, metal, temp,
                                     ampacity_table=three_ten_17) == expected


class TestGetAmbientTempDerate:
    """Tests of the get_ambient_temp_derate function."""

    @pytest.mark.parametrize("amb_temp,wire_temp,expctd",
                             [(32, 90, 0.983192),
                              (43.5, 90, 0.88034),
                              (23.2, 90, 1.055146),
                              (43.5, 75, 0.83666),
                              (43.5, 60, 0.74162),
                              (0, 60, 1.414213),
                              (-5, 60, 1.47196)])
    def test_typical_inputs(self, amb_temp, wire_temp, expctd):
        """Test typical input values."""
        ambient_temp_derate = osd.get_ambient_temp_derate(amb_temp, wire_temp)
        assert ambient_temp_derate == pytest.approx(expctd)

    def test_warn_ambient_over_wire_rating(self):
        """Raise warning if the ambient temp is greater than cable rating."""
        with pytest.warns(UserWarning):
            osd.get_ambient_temp_derate(90, 90)


class TestGetOcpd:
    """Tests of the get_ocpd function."""

    def test_dc(self):
        """Test DC circuit."""
        # current is 93.75, next OCPD is 100
        assert osd.get_ocpd(60, 'DC', ocpd_derate=0.8) == 100
        # current is 75.0, next OCPD is 80
        assert osd.get_ocpd(60, 'DC', ocpd_derate=1.0) == 80
        # current is 437.5, next OCPD is 450
        assert osd.get_ocpd(280, 'DC', ocpd_derate=0.8) == 450

    def test_ac(self):
        """Test AC circuit."""
        assert osd.get_ocpd(60, 'AC', ocpd_derate=0.8) == 80
        assert osd.get_ocpd(60, 'AC', ocpd_derate=1.0) == 60

    def test_below_ten(self):
        """Test that currents less than 10 are set to 10A."""
        assert osd.get_ocpd(9.999, 'DC', ocpd_derate=0.8) == 20


class TestGetCableSizingOcpd:
    """Tests of the get_cable_sizing_ocpd function."""

    def test_below_eight_hundred(self):
        """Test for ocpd sizes less than 800."""
        assert osd.get_cable_sizing_ocpd(80) == 70
        assert osd.get_cable_sizing_ocpd(20) == 15
        assert osd.get_cable_sizing_ocpd(800) == 700

    def test_above_eight_hundred(self):
        """Test for ocpd sizes greater than 800."""
        assert osd.get_cable_sizing_ocpd(1000) == 1000
        assert osd.get_cable_sizing_ocpd(2500) == 2500

    def test_warn_lookup_out_of_table(self):
        """Test for ocpd sizes above and below the standard sizes."""
        with pytest.warns(UserWarning):
            osd.get_cable_sizing_ocpd(10)
        with pytest.warns(UserWarning):
            osd.get_cable_sizing_ocpd(6000.1)

# ac_circ = osd.Circuit(name='inv01', start='INV.01', end='PV.PNLBD.01',
#                       voltage=480, current=28.9, length=165, parallel_sets=1,
#                       ccc_count=3, height_above_roof=3.5,
#                       temp_high_amb=97, cond_metal='Al',
#                       cond_insulation='THWN-2',
#                       cond_size=None, egc_metal='Cu', egc_size_base=None,
#                       neutral=1,
#                       conduit_size_SF=1.3, conduit_type='EMT')
#
# class OsdTests(unittest.TestCase):
#     """Tests for osd.py."""
#     def test_rooftop_adder(self):
#         roof_adders = [(0.5, 60), (0.501, 40), (3.5, 40), (3.501, 30),
#                        (12, 30),
#                        (12.01, 25), (36, 25), (36.01, 0)]
#         for height_temp_adder_pair in roof_adders:
#             print('########################')
#             print(height_temp_adder_pair)
#             ac_circ.height_above_roof = height_temp_adder_pair[0]
#             print('height above roof: {}'.format(ac_circ.height_above_roof))
#             temp = height_temp_adder_pair[1] + ac_circ.temp_high_amb
#             print('check temp: {}'.format(temp))
#             self.assertEqual(temp,
#                              ac_circ._get_amb_temp_plus_rooftop_adder(),
#                              'amb_temp: {}, height above roof: {},\
#                               amb + rooftop adder: {}'.format(
#                               ac_circ.temp_high_amb,
#                               ac_circ.height_above_roof,
#                               ac_circ._get_amb_temp_plus_rooftop_adder()))
#
#     def test_amb_temp_corr(self):
#         ac_circ.height_above_roof = 3
#         ac_circ.temp_high_amb = 97
#         self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.72648)
#
#         ac_circ.height_above_roof = 3
#         ac_circ.temp_high_amb = 95
#         self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.73912)
#
#         ac_circ.height_above_roof = 3
#         ac_circ.temp_high_amb = 88
#         self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.78174)
#
#         ac_circ.height_above_roof = 3
#         ac_circ.temp_high_amb = 101
#         self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.70053)
#
#     def test_cond_per_raceway_derate(self):
#         cond_derates = [(3,1),(4,0.8),(6,0.8),(7,0.7),(9,0.7),(10,0.5),
#                         (20,0.5),(21,0.45),(30,0.45),(31,0.4),(40,0.4),
#                         (41,0.35)]
#         for pair in cond_derates:
#             ac_circ.ccc_count = pair[0]
#             self.assertEqual(pair[1], ac_circ._cond_per_raceway_derate(),
#                              'Conductors per conduit derate test')
#
# if __name__ == '__main__':
#     unittest.main()
