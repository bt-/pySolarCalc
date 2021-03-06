import pytest
import osd
import nec_tables as nec


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
