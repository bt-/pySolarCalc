import warnings
import nec_tables as nec


def lookup(lookup_value, table, keys=True):
    """
    Perform lookup in NEC table using a numeric value.

    Returns the next highest value when the `lookup_value` does not match a
    value in the table.

    Parameters
    ----------
    lookup_value : numeric
        Value to compare against values within the passed table.
    table : dictionary or list
        The NEC table to perform the lookup against. Import tables from
        nec_tables module.  Many tables are nested and require indexing into
        before passing to this function.
    keys : bool, default True
        If true, compares the `lookup_value`against the `table` keys.
        If false, compares the `lookup_value` against the `table` values.

    """
    table_is_dict = isinstance(table, dict)
    if table_is_dict:
        if not keys:
            table = {val: key for key, val in table.items()}
        vals_to_compare = list(table.keys())
    else:
        vals_to_compare = table

    if lookup_value > vals_to_compare[-1]:
        return warnings.warn('Lookup value is outside of the table.')

    for val in vals_to_compare:
        # print('i: {}, value: {}'.format(i, val))
        if lookup_value <= val:
            # key = val
            if table_is_dict:
                return table[val]
            else:
                return val


def get_wire_ampacity(size, metal, wire_insulation_temp, current=None,
                      derates=1.0, ampacity_table='310_B_16'):
    """
    Lookup ampacity of wire size or check ampacity against passed current.

    By default, function looks up the ampacity for a given conductor size from
    an NEC ampacity table given a wire material, insulation temperature rating,
    and the ampacity table.

    Can also be used to return a boolean to check if the ampacity of the cable
    exceeds a given current.

    Use the lookup function to perform the reverse - find a wire size for a
    given current.

    Parameters
    ----------
    size : str
        Wire size, which must be an exact match of a wire size in the table.
    metal : str
        Type of metal used as the curent carrying conductor. Must be in the
        table passed.
        'Cu' or 'Al'
    wire_insulation_temp : numeric
        Temperature rating of the conductor insulation. Must be in the table.
        Typically, 60, 75, or 90.
    current : numeric, default None
        Default of None, returns ampacity of the conductor.
        Pass numeric current value to check if the ampacity of the conductor
        exceeds the passed current.
    derates : numeric, default 1.0
        Derating to be applied to the looked up ampacity.
    ampacity_table : str, default '310_B_16'
        String name for ampacity tables. See keys of the ampacity_tables
        dictionary in the nec_tables for available ampacity tables.

    Returns
    -------
    ampacity : numeric
        Default is to return the ampacity of the conductor after applying
        derates, if any are passed.
    bool
        If a current is passed, returns True if the looked up ampacity after
        applying derates, if any are passed, is greater than the passed
        current.

    """
    ampacity_table = nec.ampacity_tables[ampacity_table]
    ampacity = ampacity_table[metal][wire_insulation_temp][size]
    if current is None:
        return ampacity * derates
    else:
        return (ampacity * derates) >= current


def get_ambient_temp_derate(ambient_temp, wire_insulation_temp,
                            table_ambient_temp=30):
    """
    Determine the cable derate required for the ambient temperature.

    NEC Reference - Equation 310.15(B)(2)
    Function uses the equation to calculate the ambient temperature derate
    rather than Table 310.15(B)(2)(a), 30C ambient, or
    Table 310.15(B)(2)(b), 40C ambient.

    Parameters
    ----------
    ambient_temp : numeric
        The ambient temperature in degrees Celsius.
    wire_insulation_temp : numeric
        Wire insulation temperature rating in degrees Celsius.
        Typically 60, 75, or 90.
    table_ambient_temp : numeric, default 30
        Ambient temperature of the the table used to look up conductor
        ampacity. Table 310.15(B)(16) is the most commonly used table to lookup
        conductor ampacities and is based on 30C, thus the 30C default value.

    Returns
    -------
    float
        The derate required for the ambient temperature.

    """
    if ambient_temp >= wire_insulation_temp:
        return warnings.warn('Ambient temperature should not equal or '
                             'exceed cable rating.')

    return(((wire_insulation_temp - ambient_temp) /
            (wire_insulation_temp - table_ambient_temp)) ** 0.5)


def get_ocpd(current, voltage_type, ocpd_derate=0.80):
    """
    Determine overcurrent protection device (OCPD) size.

    NEC Reference
    690.8(A)(1)(1) for DC current
    NEC 240.6 for use of next largest OCPD for currents less than 800A
    240.6(A) for standard OCPD sizes

    Parameters
    ----------
    current : numeric
        Operating current for the circuit in amps.
    voltage_type : str
        Either 'AC' or 'DC' indicating circuit carries alternating or direct
        current.
    ocpd_derate : numeric, default 0.8
        Rating of the overcurrent protective device. Usually 0.8 or 1.

    """
    if current < 10:
        current = 10

    if voltage_type == 'DC':
        current = current * 1.25

    design_current = current / ocpd_derate
    return lookup(design_current, nec.ocpd_sizes)


def get_cable_sizing_ocpd(ocpd):
    """
    Get next smallest standard OCPD size if OCPD is less than 800A.

    NEC Reference - 240.4(B) and (C)

    Parameters
    ----------
    ocpd : numeric
        The ocpd size to be used to protect the circuit.

    Returns
    -------
    next_smallest_ocpd : numeric
        The next smallest standard ocpd size to be used for checking cable
        ampacity.

    """
    if ocpd < nec.ocpd_sizes[0] or ocpd > nec.ocpd_sizes[-1]:
        warnings.warn('OCPD size passed is above or below the standard '
                      'OCPD sizes.')

    if ocpd <= 800:
        for i, standard_ocpd in enumerate(nec.ocpd_sizes):
            if standard_ocpd == ocpd:
                return nec.ocpd_sizes[i - 1]
    else:
        return ocpd

# class Circuit(object):
#     """docstring for circuits.
#     parent class for dc and ac circuits
#     Attributes
#     ----------
#     name: string
#     start: string
#         originating equipment of the circuit
#     end: string
#         terminating equipment of the circuit
#     voltage: int
#         design voltage for circuit- 480, 277, 120, 12470
#     current: float
#     length: float
#         length of circuit in feet
#     parallel_sets: int
#         number of paralle sets of conductors
#     ccc_count: int
#         Current carrying conductors per conduit. Does not include neutral.
#         For the conditions of use derate calculations
#     height_above_roof: float
#         height above roof in inches
#     temp_high_amb: float
#         Degrees Fahrenheit
#         Recommended ASHRAE design 2 percent high
#         Passed by parent class in future?
#     cond_material: string
#         Conductor metal as "Cu" or "Al"
#     cond_insulation: string
#         Conductor insulation type
#     cond_size_base: string
#     egc_material: string
#         Equipment ground condcutor metal as "Cu" or "Al"
#     egc_size_base: string
#         Equipment ground condcutor size
#     neutral: int
#         Use 1 to include neutral in conduit size calculation.
#         Integer > 1 to add condcutors the same size as the currenty carrying
#     conduit_size_SF: float
#         Safety factor for conduit size calculation.
#         Default is 1.3
#     conduit_type: string
#
#     Internal Attributes
#     ___________________
#     ocpd
#     rooftop_adder
#     cond_size_base
#     egc_size_base
#     v_drop_volts
#     v_drop_percent
#     v_drop_in_range
#     conduit_size
#
#     """
#     def __init__(self, name=None, start=None, end=None,
#                  voltage=None, current=None, length=None, parallel_sets=1,
#                  ccc_count=3, height_above_roof=3.5, temp_high_amb=None,
#                  cond_metal=None, cond_insulation=None, cond_size=None,
#                  egc_metal='Cu', egc_size_base=None, neutral=1,
#                  conduit_size_SF=1.3,
#                  conduit_type='EMT'):
#         super(Circuit, self).__init__()
#         self.name = name
#         self.start = start
#         self.end = end
#         self.voltage = voltage
#         self.current = current
#         self.length = length
#         self.parallel_sets = parallel_sets
#         self.ccc_count = ccc_count
#         self.height_above_roof = height_above_roof
#         self.temp_high_amb = temp_high_amb
#         self.cond_metal = cond_metal
#         self.cond_insulation = cond_insulation
#         self.cond_size = cond_size
#         self.egc_metal = egc_metal
#         self.egc_size_base = egc_size_base
#         self.neutral = neutral
#         self.conduit_size_SF = conduit_size_SF
#         self.conduit_type = conduit_type
#
#         self.ocpd = lookup(self.current * 1.25, nec_tables.ocpd_sizes)
#
#     def _update_attribute(self, arg):
#         """
#         Set attribute and recalulate dependent values.
#         """
#         pass
#
#     def _get_amb_temp_plus_rooftop_adder(self):
#         """[Needs to be updated]
#         Table removed in NEC 2017 (now only a single value), valid for 2008,
#         2011, 2014
#         Temperatures in Fahrenheit
#         """
#         if self.height_above_roof == -1:
#             return self.temp_high_amb
#         elif self.height_above_roof <= 0.5:
#             return self.temp_high_amb + 60
#         elif self.height_above_roof <= 3.5:
#             return self.temp_high_amb + 40
#         elif self.height_above_roof <= 12:
#             return self.temp_high_amb + 30
#         elif self.height_above_roof <= 36:
#             return self.temp_high_amb + 25
#         elif self.height_above_roof > 36:
#             return self.temp_high_amb + 0
#
#     def get_amb_temp_derate(self):
#         """Write method to use the top level function."""
#         pass
#
#     def _cond_per_raceway_derate(self):
#         """[Needs to be updated]
#         NEC 310.15(B)(3)(a) Adjustment factors for more than three
#         current-carrying conductors in a raceway or cable
#         """
#         if self.ccc_count < 4:
#             return(1.0)
#         elif self.ccc_count <= 6:
#             return(0.8)
#         elif self.ccc_count <= 9:
#             return(0.7)
#         elif self.ccc_count <= 20:
#             return(0.5)
#         elif self.ccc_count <= 30:
#             return(0.45)
#         elif self.ccc_count <= 40:
#             return(0.4)
#         elif self.ccc_count >= 41:
#             return(0.35)
#
#
# class DcCircuit(Circuit):
#     """docstring for DcCircuit.
#     Class for AC circuits.
#
#     """
#     def __init__(self, name=None, ccc_count=2):
#         super(DcCircuit, self).__init__()
#         self.name = name
#         self.ccc_count = ccc_count
#
# class AcCircuit(Circuit):
#     """docstring for AcCircuit.
#     Class for AC circuits.
#     """
#     def __init__(self, arg):
#         super(AcCircuit, self).__init__()
#         self.arg = arg
#
# if __name__ == '__main__':
#     main()
