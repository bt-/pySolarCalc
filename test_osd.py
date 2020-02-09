import unittest
import pytest
import osd


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








ac_circ = osd.Circuit(name='inv01', start='INV.01', end='PV.PNLBD.01',
                      voltage=480, current=28.9, length=165, parallel_sets=1,
                      ccc_count=3, height_above_roof=3.5,
                      temp_high_amb=97, cond_metal='Al', cond_insulation='THWN-2',
                      cond_size=None, egc_metal='Cu', egc_size_base=None, neutral=1,
                      conduit_size_SF=1.3, conduit_type='EMT')

class OsdTests(unittest.TestCase):
    """Tests for osd.py."""
    def test_rooftop_adder(self):
        roof_adders = [(0.5, 60), (0.501, 40), (3.5, 40), (3.501, 30), (12, 30),
                       (12.01, 25), (36, 25), (36.01, 0)]
        for height_temp_adder_pair in roof_adders:
            print('########################')
            print(height_temp_adder_pair)
            ac_circ.height_above_roof = height_temp_adder_pair[0]
            print('height above roof: {}'.format(ac_circ.height_above_roof))
            temp = height_temp_adder_pair[1] + ac_circ.temp_high_amb
            print('check temp: {}'.format(temp))
            self.assertEqual(temp, ac_circ._get_amb_temp_plus_rooftop_adder(),
                             'amb_temp: {}, height above roof: {},\
                              amb + rooftop adder: {}'.format(
                              ac_circ.temp_high_amb,
                              ac_circ.height_above_roof,
                              ac_circ._get_amb_temp_plus_rooftop_adder()))

    def test_amb_temp_corr(self):
        ac_circ.height_above_roof = 3
        ac_circ.temp_high_amb = 97
        self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.72648)

        ac_circ.height_above_roof = 3
        ac_circ.temp_high_amb = 95
        self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.73912)

        ac_circ.height_above_roof = 3
        ac_circ.temp_high_amb = 88
        self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.78174)

        ac_circ.height_above_roof = 3
        ac_circ.temp_high_amb = 101
        self.assertEqual(round(ac_circ._amb_temp_correction(),5), 0.70053)

    def test_cond_per_raceway_derate(self):
        cond_derates = [(3,1),(4,0.8),(6,0.8),(7,0.7),(9,0.7),(10,0.5),
                        (20,0.5),(21,0.45),(30,0.45),(31,0.4),(40,0.4),
                        (41,0.35)]
        for pair in cond_derates:
            ac_circ.ccc_count = pair[0]
            self.assertEqual(pair[1], ac_circ._cond_per_raceway_derate(),
                             'Conductors per conduit derate test')

if __name__ == '__main__':
    unittest.main()
